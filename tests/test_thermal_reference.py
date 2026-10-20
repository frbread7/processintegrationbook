"""Independent reference calculation for the displayed one-dimensional model.

This intentionally does not import the JavaScript implementation. Constants and
the analytical result are fixed here so the browser implementation is checked
against a separately evaluated equation path.
"""

import math
import unittest

CONCENTRATION_EFFECTS_CAUTION_CM3 = 2e19


def independent_profile_cm3(x_nm, dose_cm2, sigma_nm, rp_nm):
    scale = dose_cm2 / (math.sqrt(2 * math.pi) * (sigma_nm / 1e7))
    sigma = sigma_nm
    return scale * (
        math.exp(-((x_nm - rp_nm) ** 2) / (2 * sigma**2))
        + math.exp(-((x_nm + rp_nm) ** 2) / (2 * sigma**2))
    )


def independent_peak_cm3(dose_cm2, sigma0_nm, holds, rp_nm=0):
    """Re-evaluate the displayed equations without importing the JS model."""
    k_b = 8.617333262145e-5
    theta_cm2 = sum(
        0.76 * math.exp(-3.46 / (k_b * (temp_c + 273.15))) * duration_s
        for temp_c, duration_s in holds
    )
    sigma0_cm = sigma0_nm / 1e7
    sigma_final_cm = math.sqrt(sigma0_cm**2 + 2 * theta_cm2)
    if rp_nm <= sigma_final_cm * 1e7:
        mode_nm = 0.0
    else:
        lo, hi = 0.0, rp_nm
        for _ in range(100):
            mid = (lo + hi) / 2
            if rp_nm * math.tanh(mid * rp_nm / (sigma_final_cm * 1e7) ** 2) > mid:
                lo = mid
            else:
                hi = mid
        mode_nm = (lo + hi) / 2
    return independent_profile_cm3(mode_nm, dose_cm2, sigma_final_cm * 1e7, rp_nm)


class ThermalReferenceTest(unittest.TestCase):
    def test_reference_scenario(self):
        k_b = 8.617333262145e-5  # eV/K
        d0 = 0.76  # cm^2/s
        ea = 3.46  # eV
        temperature_k = 1050 + 273.15
        duration_s = 20.0
        diffusivity = d0 * math.exp(-ea / (k_b * temperature_k))
        theta_cm2 = diffusivity * duration_s

        sigma0_cm = 20.0e-7
        sigma_final_cm = math.sqrt(sigma0_cm**2 + 2 * theta_cm2)
        sigma_final_nm = sigma_final_cm * 1e7
        dose_cm2 = 2.0e13
        background_cm3 = 1.0e16
        peak_cm3 = independent_peak_cm3(dose_cm2, 20, [(1050, 20)], 80)
        lo, hi = 80.0, 80.0 + 20 * sigma_final_nm
        for _ in range(100):
            mid = (lo + hi) / 2
            if independent_profile_cm3(mid, dose_cm2, sigma_final_nm, 80) > background_cm3:
                lo = mid
            else:
                hi = mid
        crossing_nm = (lo + hi) / 2

        self.assertAlmostEqual(diffusivity, 5.03425859324e-14, delta=1e-24)
        self.assertAlmostEqual(sigma_final_nm, 24.522853499, delta=1e-8)
        self.assertAlmostEqual(peak_cm3, 3.2536367e18, delta=1e11)
        self.assertAlmostEqual(crossing_nm, 163.413350077, delta=1e-6)
        self.assertLessEqual(peak_cm3, CONCENTRATION_EFFECTS_CAUTION_CM3)

    def test_concentration_caution_boundary_and_reviewer_edge_case(self):
        threshold = CONCENTRATION_EFFECTS_CAUTION_CM3
        denominator = math.sqrt(2 * math.pi) * (100 / 1e7) / 2
        dose_at_threshold = threshold * denominator
        at_threshold = independent_peak_cm3(dose_at_threshold, 100, [])
        self.assertAlmostEqual(at_threshold / threshold, 1.0, delta=1e-14)
        self.assertFalse(at_threshold > threshold)

        below = independent_peak_cm3(dose_at_threshold * (1 - 1e-9), 100, [])
        above = independent_peak_cm3(dose_at_threshold * (1 + 1e-9), 100, [])
        self.assertLess(below, threshold)
        self.assertFalse(below > threshold)
        self.assertGreater(above, threshold)
        self.assertTrue(above > threshold)

        reviewer_edge = independent_peak_cm3(1e15, 0.5, [(850, 0.1)], 80)
        self.assertGreater(reviewer_edge, 7.8e21)
        self.assertLess(reviewer_edge, 8.1e21)
        self.assertTrue(reviewer_edge > threshold)

    def test_diffusivity_ordering_is_monotonic_for_positive_activation_energy(self):
        k_b = 8.617333262145e-5
        d0, ea = 0.76, 3.46
        low = d0 * math.exp(-ea / (k_b * (850 + 273.15)))
        high = d0 * math.exp(-ea / (k_b * (1100 + 273.15)))
        self.assertGreater(high, low)

    def test_reflected_profile_conserves_dose_and_has_zero_surface_gradient(self):
        for rp_nm, sigma_nm in [(0, 20), (10, 20), (80, 20)]:
            dose, h = 2e13, 1e-6
            c0 = independent_profile_cm3(0, dose, sigma_nm, rp_nm)
            ch = independent_profile_cm3(h, dose, sigma_nm, rp_nm)
            slope = (ch - c0) / h
            self.assertLess(abs(slope) / c0, 3e-8)
            upper = rp_nm + 12 * sigma_nm
            steps = 20000
            dx = upper / steps
            total = sum(
                (1 if i in (0, steps) else 4 if i % 2 else 2)
                * independent_profile_cm3(i * dx, dose, sigma_nm, rp_nm)
                for i in range(steps + 1)
            ) * (dx / 1e7) / 3
            self.assertAlmostEqual(total / dose, 1.0, delta=1e-8)


if __name__ == "__main__":
    unittest.main()
