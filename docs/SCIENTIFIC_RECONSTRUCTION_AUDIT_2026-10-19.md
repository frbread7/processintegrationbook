# ProcessIntegrationBook scientific reconstruction audit — 2026-10-19

## Scope and status

This records the completed read-only Stage A scientific audit of the existing ProcessIntegrationBook baseline. It is an audit and reconstruction plan, not a completed reconstruction. The book covers cross-module technology decisions: requirements, integration architecture, sequence and interfaces, qualification, and evidence. BCD/LDMOS specialization belongs in PMICBook; this reconstruction should not duplicate it.

The auditor inspected the English and Korean chapter pairs, three lab experiences, model and site code, tests, and cited sources. A subsequent read-only model-assisted technical comparison inspected the full meaning of all 13 English/Korean chapter pairs, including assumptions, chronology, examples, and quizzes; it is not a human/native-language certification. Tests were inspected but **not run** at this baseline stage. No fab or silicon validation occurred. This audit does not claim full-text access beyond the specific source locations stated below, rights clearance, or completed reconstruction.

## Inventory and ten-dimension assessment

There are 13 paired chapter files at `content/en/chapters/` and `content/ko/chapters/`. Dimensions, in order, are scientific correctness (C), technical depth (D), completeness (Comp), mathematics (M), source evidence (S), physical consistency (P), numerical model (N), visuals (V), bilingual meaning (B), and educational usefulness (U). **S** means sound, **L** means limited, **G** means a gap, **—** means not applicable/limited relevance, and **?** means semantic parity was not fully established.

The received audit record labels this an exact ten-dimension matrix, but supplies 11 ratings for c06 and c13. I preserve those two raw sequences below instead of silently dropping a rating. A separate, explicit ten-dimension reassessment appears below; it does not pretend to recover the original intent of the extra raw token.

| Chapter file | Section IDs observed | Raw C/D/Comp/M/S/P/N/V/B/U ratings | Focused reconstruction plan |
| --- | --- | --- | --- |
| `c01-integration-as-decision.html` | `decision-question`, `objectives`, `decision-record`, `worked-decision`, `evidence-labels`, `knowledge-check`, `further-reading` | `S/L/L/—/L/S/—/G/?/S` | Retain the decision-record framing; strengthen evidence sourcing and technical depth with a bounded, traceable worked decision, clarify EN/KO semantic parity, and add a useful visual for the decision/evidence chain. |
| `c02-requirements-to-architecture.html` | `architecture-question`, `objectives`, `requirements-stack`, `architecture-portfolio`, `worked-architecture`, `architecture-limits`, `knowledge-check`, `further-reading` | `S/L/L/—/L/S/—/G/?/S` | Deepen the requirements-to-portfolio comparison with explicit interface constraints and evidence for trade-offs; add a diagram of the architecture allocation and align its explanation in Korean. |
| `c03-sequence-interface-contracts.html` | `sequence-question`, `objectives`, `state-contracts`, `dependency-types`, `worked-sequence`, `sequence-limits`, `knowledge-check`, `further-reading` | `S/L/L/—/L/S/—/G/?/S` | Add a sourced, worked typed-dependency example that makes entry/exit state and invalid sequencing visible; diagram the contract graph and review translation parity. |
| `c04-isolation-substrate-choices.html` | `chapter-title` only | `S/L/L/—/L/S/—/G/?/S` | Preserve the shared-interface decision scope. Add stable semantic anchors, strengthen sourced comparison of isolation/substrate choices and a worked decision, and provide a visual comparison. |
| `c05-gate-stack-architecture.html` | `chapter-title` only | `S/L/L/—/S/S/—/L/?/S` | Preserve the sourced stack/flow coupling. Expand the worked architecture decision and interface/thermal evidence, add section anchors, and assess whether a diagram would clarify process order. |
| `c06-junction-thermal-history.html` | `c06-objectives` | `G/S/L/G/S/G/G/L/S/?/S` (11 entries supplied) | Repair the model's surface-dose interpretation and plot range (P1 findings below). Keep the stated equilibrium/dilute limitations explicit; add a counterexample demonstrating why a non-isothermal history is not interchangeable with a simple order-invariant or mean-temperature shortcut. Clarify Korean semantic parity in the full reconstruction. |
| `c07-pattern-transfer-chain.html` | None observed | `S/L/L/L/L/S/L/G/?/S` | Add stable anchors and deepen the sourced pattern-transfer/error-budget worked choice. Add a visual of feature-state propagation across lithography, etch, and planarization; check EN/KO parity. |
| `c08-contact-mol-interface.html` | None observed | `S/L/L/L/L/S/—/G/?/S` | Add stable anchors and a sourced, quantitative-enough current-path/interface worked decision; provide a contact/MOL interface diagram and verify the Korean technical meaning. |
| `c09-beol-compatibility.html` | None observed | `S/L/L/L/L/S/—/G/?/S` | Add stable anchors, deepen the thermal/plasma/topography inheritance example with source-linked qualification evidence, and diagram the stack compatibility chain. Preserve its integration scope. |
| `c10-variation-propagation.html` | `variation-propagation`, `c10-objectives`, `c10-chain`, `c10-worked`, `c10-evidence`, `c10-check`, `c10-reading` | `S/L/L/L/L/S/—/G/?/S` | Improve the sourced propagation chain and worked distinction between contact-resistance and transistor shifts; add a visual showing shared state and dependence rather than an unqualified list of sigmas. |
| `c11-design-technology-cooptimization.html` | `dtco`, `c11-objectives`, `c11-loop`, `c11-worked`, `c11-limits`, `c11-check`, `c11-reading` | `S/L/L/—/L/S/—/G/?/S` | Strengthen source-backed DTCO trade-offs and the robust-cell example; diagram the feedback loop and state assumptions/limits in both languages. |
| `c12-integration-learning-qualification.html` | `learning-qualification`, `c12-objectives`, `c12-evidence`, `c12-worked`, `c12-limits`, `c12-check`, `c12-reading` | `S/L/L/—/L/S/—/G/?/S` | Develop the concern-to-evidence gate and controlled-change example with explicit qualification evidence, sources, and a visual change/evidence path. Check EN/KO parity. |
| `c13-public-platform-case.html` | `public-platform-case`, `c13-objectives`, `c13-source`, `c13-integration-questions`, `c13-worked`, `c13-evidence-limits`, `c13-check`, `c13-reading` | `S/S/L/—/S/S/—/G/S/?/S` (11 entries supplied) | Preserve the historically bounded public case and explicit evidence/inference boundary. Add a visual sequence and connect the reported flow to the worked integration questions without generalizing it to a universal platform. Confirm the extra matrix entry and Korean parity in review. |

Across chapters, the auditor found identical EN/KO section ID and link sequences and matching numeric tokens. Chapters contain zero figures/SVGs; c05 has one table; c06 has three math blocks; c10 has one. English chapter lengths range from 592 to 987 words. The supplied matrix shows visual gaps across most chapters and limited technical depth/completeness; those are baseline gaps, not a claim that every chapter needs more prose. Prefer focused worked evidence and useful diagrams.

### Independent ten-dimension reassessment and full-pair semantic inspection

The following is a **new baseline reassessment**, not a recovered interpretation of the two malformed raw rows. The raw c06 and c13 sequences above remain intact. For both, the ninth raw `S` is an unassigned anomalous token; the original auditor's intended mapping cannot be proven. The reassessment used the actual chapter text and the physical/code findings: c06 has a surface-dose/model inconsistency and limited visualization, while c13 has no chapter figure at baseline and a bounded public chronology. The ten ordered values below are C, D, Comp, M, Source, Physical, Numeric, Visual, Bilingual, Usefulness. Bilingual ratings reflect a separate substantive read-only comparison of the complete 13 paired chapter bodies, including equations, qualifiers, process order, examples, and quiz answers. They do not establish human translation certification or future parity after edits.

| Chapter | Ten reassessed baseline values | EN/KO semantic disposition and exact baseline locator |
| --- | --- | --- |
| c01 | `S/L/L/—/L/S/—/G/S/S` | Sound: decision record, evidence labels, alternatives, and quiz agree; `#decision-record`, `#worked-decision`. |
| c02 | `S/L/L/—/L/S/—/G/S/S` | Sound: hard requirements, portfolio alternatives, split logic, and limits agree; `#requirements-stack`, `#worked-architecture`. |
| c03 | `S/L/L/—/L/S/—/G/S/S` | Sound: entry/exit states, typed dependencies, and graph limits agree; `#state-contracts`, `#worked-sequence`. |
| c04 | `S/L/L/—/L/S/—/G/L/S` | Limited: KO `평탄도 한계` narrows EN *topography limits*; `c04-isolation-substrate-choices.html`, interface and worked-decision sections (unanchored at baseline). |
| c05 | `S/L/L/—/S/S/—/L/S/S` | Sound: gate-order choices and reported-versus-inferred qualifiers agree; `c05-gate-stack-architecture.html#chapter-title`. |
| c06 | `G/S/L/G/S/G/G/L/G/S` | Gap: KO `일정한 D` can imply temperature invariance, `과도 확산` drops *enhanced* from transient-enhanced diffusion, and the surface-truncation premise was not stated as a model assumption; `c06-junction-thermal-history.html#c06-objectives` and profile/limits sections. The model defect is common to both languages. |
| c07 | `S/L/L/L/L/S/L/G/L/S` | Limited: KO quiz `위치별 에지 배치` loses *location-correlated*; the shared landing/contact enclosure direction was ambiguous; `c07-pattern-transfer-chain.html` error-budget and quiz sections (unanchored at baseline). |
| c08 | `S/L/L/L/L/S/—/G/S/S` | Sound: contact/current path, extraction limits, and quiz agree; `c08-contact-mol-interface.html`, unanchored baseline sections. |
| c09 | `S/L/L/L/L/S/—/G/G/S` | Gap: KO says thinner barrier reduces fill area, reversing EN, and mistranslates *censored failures* as below-detection failures; `c09-beol-compatibility.html`, worked and qualification sections (unanchored at baseline). |
| c10 | `S/L/L/L/L/S/—/G/S/S` | Sound: sensitivity/covariance qualifiers and contact-versus-transistor example agree; `#c10-chain`, `#c10-worked`. |
| c11 | `S/L/L/—/L/S/—/G/S/S` | Sound: DTCO loop and robust-cell scenario agree; `#c11-loop`, `#c11-worked`. |
| c12 | `S/L/L/—/L/S/—/G/L/S` | Limited: KO *null result* can read as no result rather than measured no-change, and material genealogy loses lot/wafer lineage; `#c12-evidence`. |
| c13 | `S/S/L/—/S/S/—/G/L/S` | Limited: KO omits *contact* from CESL and calls a constructed worked analysis an `실제` historical decision; `#c13-source`, `#c13-worked`. The Mistry sequence itself agrees. |

These baseline translation findings are actionable reconstruction targets. Full-pair comparison was model-assisted and performed during candidate edits for c04–c07; final parity must be repeated on a frozen candidate source tree. The c06/c13 raw-rating anomaly remains a data-quality finding, not a scientific defect.

## Three implemented lab experiences

| Location/anchor | Observed scope |
| --- | --- |
| `site/lab.html#thermal-lab` and `site/ko/lab.html#thermal-lab`; model `site/labs/thermal-model.js` | Numerical thermal-history and Gaussian profile estimate; assumptions and limitations are described in c06. |
| `#dependency-explorer` | Three fixed dependency cases; this is a fixed-case explorer, not a general process-flow simulator. |
| `#integration-review` | Three fixed integration choices; this is a bounded review aid, not an automated engineering disposition. |

## P1 findings

### Surface truncation makes the dose interpretation inconsistent near the surface

The c06 text and model define `Q` as an implanted areal dose but calculate a full-line Gaussian centered at projected range `Rp`. For the physical silicon domain `x ≥ 0`, the integrated dose represented by that profile is `Q Φ(Rp/σf)` (where Φ is the standard normal CDF), not Q. At `Rp=0` it is exactly `0.5Q`; at the default parameters it is approximately `0.99946Q`. Thus the stated “far enough below the surface” approximation is sensible for the default, but the accepted `Rp=0` boundary is not dose-conserving. The model already flags likely surface truncation when `Rp < 3σf` but continues to report the untruncated profile.

Evidence paths: `content/en/chapters/c06-junction-thermal-history.html:30-36` and `site/labs/thermal-model.js:29-68`. Focused repair: either model a normalized/truncated implant profile for the half-space, or reject/clearly mark inputs where truncation is material and label the profile integral as an approximation. Keep the meaning of Q, peak concentration, and threshold crossing consistent. Add boundary validation around `Rp/σf`; do not present this scenario model as calibrated process data.

### The plotted depth can omit the calculated crossing

For valid inputs `σ₀=100 nm`, `Rp=500 nm`, `Q=1×10¹⁵ cm⁻²`, `NB=1×10¹⁴ cm⁻³`, and thirty 3600-second holds at 1100 °C, the model gives `σf≈1815 nm` and `x*≈8615 nm`. The chart chooses the displayed maximum depth from `Rp + 4.5σf` but caps it at 1000 nm, so it omits the calculated crossing and much of the profile for this valid case.

Evidence path: `site/assets/site.js:181-212`. Focused repair: make the chart range include the reported crossing and enough of the profile, or communicate clearly when the plotted interval is clipped. Preserve legible axes and verify the computed crossing is visible for valid inputs.

## P2 findings

- **Blank projected range input:** `Number("")` becomes zero in the browser input parsing path, so an empty Rp field is accepted as `Rp=0` (`site/assets/site.js:112-123`). Distinguish blank from numeric zero and return a validation message for blank input.
- **Depth and figures:** there are no chapter figures/SVGs and most chapters have limited depth/completeness in the audit matrix. Add only diagrams that explain integration relationships, state/sequence, or evidence; do not pad chapters with decorative art.
- **Defect morphology versus origin:** add a focused worked case distinguishing observed defect morphology from hypothesized origin, with evidence needed to discriminate hypotheses. This supports the book's evidence-based integration decisions and should not imply morphology alone proves cause.
- **Thermal-order approximation:** demonstrate with a bounded counterexample why `Θ=ΣD(Tᵢ)tᵢ` is order-invariant under the model's shared constant-diffusivity assumptions, while real sequence changes in ambient, interfaces, point defects, or mechanism can make that simplification inapplicable. Keep this within c06's stated limits.
- **Stable anchors:** c04–c09 have only a title anchor (c04/c05/c06) or no section IDs (c07–c09). Add stable semantic IDs in both languages so cross-links and review references remain traceable.

## Reproducible numerical observations and source evidence

The c06 model uses `D(T)=D₀ exp(−Eₐ/(kB T))`, `Θ=ΣD(Tᵢ)tᵢ`, and `σf²=σ₀²+2Θ`, with `D₀=0.76 cm²/s`, `Eₐ=3.46 eV`, and `kB=8.617333262145×10⁻⁵ eV/K`. For the documented check `σ₀=20 nm`, `Rp=80 nm`, `Q=2×10¹³ cm⁻²`, `NB=10¹⁶ cm⁻³`, and one 1050 °C, 20 s hold, the reported values are `D≈5.0343×10⁻¹⁴ cm²/s`, `σf=24.52285 nm`, and `x*≈163.41335 nm`. Dimensional consistency was confirmed from the stated equations. The first comparison uses one hold; multi-hold exposure is additive only within the declared shared-model assumptions.

The Arrhenius pair is printed on p. G387 of Esser et al. (2004). That source's reference cites Sze (1983), and Mostafa and Medraj (2017) cites Scotten (2000), but the original Sze/Scotten pages or tables were not inspected. The pair's reported value is supported by accessible publications; its precise original source provenance remains unresolved. The accessible links and source locations are recorded in [docs/REFERENCES.md](REFERENCES.md). The Mistry et al. 2007 platform sequence was checked against Figure 5 and surrounding text on pp. 247–248: ALD high-k/dummy poly before source/drain/Ni salicide; ILD polish/poly removal before workfunction metals and Al fill. This is a historical public platform report, not a universal flow. Proposed transfer implications must remain labeled as inference.

## Verification and evidence boundaries

The baseline auditor inspected all tests but did not execute them. Historical or source-level checks are not fresh test results. No fab or silicon measurements, process calibration, or production recipe validation are claimed. The two P1 observations are model/code consistency findings and reproducible calculations on allowed inputs; they do not establish defects in any manufacturing flow. A subsequent full-pair model-assisted bilingual comparison found the specific defects recorded in the reassessment, but final candidate parity still requires frozen-tree review. The c06/c13 raw sequences retain unexplained extra ratings.
