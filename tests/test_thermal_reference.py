"""Independent reference calculation for the displayed one-dimensional model.

This intentionally does not import the JavaScript implementation. Constants and
the analytical result are fixed here so the browser implementation is checked
against a separately evaluated equation path.
"""

import math
import unittest

CONCENTRATION_EFFECTS_CAUTION_CM3 = 2e19


def independent_peak_cm3(dose_cm2, sigma0_nm, holds):
    """Re-evaluate the displayed equations without importing the JS model."""
    k_b = 8.617333262145e-5
    theta_cm2 = sum(
        0.76 * math.exp(-3.46 / (k_b * (temp_c + 273.15))) * duration_s
        for temp_c, duration_s in holds
    )
    sigma0_cm = sigma0_nm / 1e7
    sigma_final_cm = math.sqrt(sigma0_cm**2 + 2 * theta_cm2)
    return dose_cm2 / (math.sqrt(2 * math.pi) * sigma_final_cm)


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
        peak_cm3 = dose_cm2 / (math.sqrt(2 * math.pi) * sigma_final_cm)
        crossing_nm = 80.0 + sigma_final_nm * math.sqrt(2 * math.log(peak_cm3 / background_cm3))

        self.assertAlmostEqual(diffusivity, 5.03425859324e-14, delta=1e-24)
        self.assertAlmostEqual(sigma_final_nm, 24.522853499, delta=1e-8)
        self.assertAlmostEqual(peak_cm3, 3.2536367e18, delta=1e11)
        self.assertAlmostEqual(crossing_nm, 163.413350077, delta=1e-6)
        self.assertLessEqual(peak_cm3, CONCENTRATION_EFFECTS_CAUTION_CM3)

    def test_concentration_caution_boundary_and_reviewer_edge_case(self):
        threshold = CONCENTRATION_EFFECTS_CAUTION_CM3
        denominator = math.sqrt(2 * math.pi) * (100 / 1e7)
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

        reviewer_edge = independent_peak_cm3(1e15, 0.5, [(850, 0.1)])
        self.assertGreater(reviewer_edge, 7.8e21)
        self.assertLess(reviewer_edge, 8.1e21)
        self.assertTrue(reviewer_edge > threshold)

    def test_diffusivity_ordering_is_monotonic_for_positive_activation_energy(self):
        k_b = 8.617333262145e-5
        d0, ea = 0.76, 3.46
        low = d0 * math.exp(-ea / (k_b * (850 + 273.15)))
        high = d0 * math.exp(-ea / (k_b * (1100 + 273.15)))
        self.assertGreater(high, low)


if __name__ == "__main__":
    unittest.main()
