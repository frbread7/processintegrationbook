# References and source use

The references support specific background claims and offer further reading; they are not blanket support for every example. Platform descriptions are dated and source-limited. No recipe, unpublished specification, or non-public data is used.

## Public papers and technical background

1. R. B. Fair, “Boron Diffusion in Silicon—Concentration and Orientation Dependence, Background Effects, and Profile Estimation,” *Journal of The Electrochemical Society*, 122(6), 800–805 (1975). [DOI: 10.1149/1.2134326](https://doi.org/10.1149/1.2134326). Discusses dependence on concentration, ambient/orientation, and background conditions; it is a reason to limit the lab to a dilute, idealized case.
2. H. Bracht, H. H. Silvestri, I. D. Sharp, and E. E. Haller, “Self- and foreign-atom diffusion in semiconductor isotope heterostructures. II. Experimental results for silicon,” *Physical Review B*, 75, 035211 (2007). [DOI: 10.1103/PhysRevB.75.035211](https://doi.org/10.1103/PhysRevB.75.035211). Reports B, As, and P diffusion experiments in silicon isotope multilayers over 850–1100 °C and discusses native point-defect contributions.
3. B. Sadigh, T. J. Lenosky, S. K. Theiss, M.-J. Caturla, T. Diaz de la Rubia, and M. A. Foad, “Mechanism of Boron Diffusion in Silicon: An Ab Initio and Kinetic Monte Carlo Study,” *Physical Review Letters*, 83(21), 4341–4344 (1999). [DOI: 10.1103/PhysRevLett.83.4341](https://doi.org/10.1103/PhysRevLett.83.4341). Presents an interstitialcy mechanism from atomistic calculations and kinetic Monte Carlo; it is not used as a process calibration.
4. Y.-C. Yeo, “Metal gate technology for nanoscale transistors—material selection and process integration issues,” *Thin Solid Films*, 462–463, 34–41 (2004). [DOI: 10.1016/j.tsf.2004.05.039](https://doi.org/10.1016/j.tsf.2004.05.039). Review of material-selection and integration questions around metal gates.
5. R. Aitken, V. Chandra, B. Cline, S. Das, D. Pietromonaco, L. Shifren, S. Sinha, and G. Yeric, “Predicting future complementary metal–oxide–semiconductor technology—challenges and approaches,” *IET Computers & Digital Techniques*, 10(6), 315–322 (2016). [DOI: 10.1049/iet-cdt.2015.0210](https://doi.org/10.1049/iet-cdt.2015.0210). Discusses predictive technology, circuit-level exploration, and design-technology co-optimization.
6. K. Mistry et al., “A 45nm Logic Technology with High-k + Metal Gate Transistors, Strained Silicon, 9 Cu Interconnect Layers, 193nm Dry Patterning, and 100% Pb-free Packaging,” in *2007 IEEE International Electron Devices Meeting*, 247–250. [DOI: 10.1109/IEDM.2007.4418914](https://doi.org/10.1109/IEDM.2007.4418914). Chapter 13 names only the disclosed platform features stated in the public paper record and treats all unreported coupling as a question or inference.
7. S. M. Sze and K. K. Ng, *Physics of Semiconductor Devices*, 3rd ed., Wiley (2007). [Publisher DOI: 10.1002/0470068329](https://doi.org/10.1002/0470068329). General semiconductor-device reference. The 0.76 cm²/s, 3.46 eV default Arrhenius pair is the conventional intrinsic boron-in-silicon teaching parameterization cited for the model, not a universal or calibrated value.

## Independent books used for scope comparison

The following repositories were inspected at pinned commits. They are independent works, not this project's publications; no content, image, code, or simulator is incorporated:

- [ProcessBook, revision f583bc3](https://github.com/geniuskey/processbook/tree/f583bc33c5dfdd31292f7ef6826ce24a2c8b7fed)
- [DopingBook, revision 944526d](https://github.com/geniuskey/dopingbook/tree/944526d6c2bb790d5d8f1e08d2614e1c5de22c3c)
- [LithoBook, revision 5a4fa0a](https://github.com/geniuskey/lithobook/tree/5a4fa0a5b79f3d5581af140caa0e7831ccf88a05)
- [EtchBook, revision 0881e61](https://github.com/geniuskey/etchbook/tree/0881e61ba16003a1fe4579a8372dad2d63d2dcfb)
- [TCADBook, revision 56d3c14](https://github.com/geniuskey/tcadbook/tree/56d3c14f757a55caed574e720069cfdf2b7a2bf6)
- [YieldBook, revision 2acd884](https://github.com/geniuskey/yieldbook/tree/2acd8844633274ebea91e808c4a22ed4035549b8)
- [PMICBook](https://github.com/frbread7/pmicbook), a separate BCD/PMIC-focused textbook.
- [WATBook](https://github.com/frbread7/watbook), a separate wafer-level measurement and parametric-engineering textbook.

The complete sampled chapter-level matrix and its limitations are in [OVERLAP_AUDIT.md](OVERLAP_AUDIT.md).
