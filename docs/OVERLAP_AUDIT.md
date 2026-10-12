# Reference overlap and differentiation audit

**Audit date:** 2026-10-12
**Purpose:** Establish the teaching boundary before authoring. This is a source inspection of public repositories, not an exhaustive claim that no other book teaches a topic.

## Decision

ProcessIntegrationBook is distinct if it owns the *cross-module technology decision layer*: translating product/device requirements into an integration architecture, tracing constraints across process interfaces and sequence, comparing candidate flows, planning discriminating evidence, and managing qualification/change decisions. It must not become another module survey, process-flow primer, device/TCAD text, WAT guide, or yield/FA handbook.

The reference collection already contains an introductory CMOS integration sequence in ProcessBook, a process-composer experiment there, and a directly relevant BCD integration chapter in PMICBook. Therefore this book will deepen the *comparison and decision method* around public examples; it will link to those works for module and product fundamentals. ProcessIntegrationBook will not reproduce their prose, figures, simulators, or process recipes.

## Inspected source revisions

The repository trees below were shallow-cloned from their public default branches on the audit date. Revision pins make the inspection reproducible; they do not imply endorsement or reuse.

| Independent reference | Inspected revision | High-relevance source pages |
|---|---|---|
| [ProcessBook](https://github.com/geniuskey/processbook) | `f583bc33c5dfdd31292f7ef6826ce24a2c8b7fed` | `chapters/integration.html`, `advanced.html`, `lab.html`, `anneal.html`, `oxidation.html`, `implant.html`, `etch.html`, `deposition.html`, `cmp.html`, `metal.html` |
| [DopingBook](https://github.com/geniuskey/dopingbook) | `944526d6c2bb790d5d8f1e08d2614e1c5de22c3c` | `chapters/flow.html`, `budget.html`, `anneal.html`, `diffusion.html`, `damage.html`, `metrology.html` |
| [LithoBook](https://github.com/geniuskey/lithobook) | `5a4fa0a5b79f3d5581af140caa0e7831ccf88a05` | `chapters/transfer.html`, `overlay.html`, `window.html`, `multipatterning.html`, `opc.html` |
| [EtchBook](https://github.com/geniuskey/etchbook) | `0881e61ba16003a1fe4579a8372dad2d63d2dcfb` | `chapters/overview.html`, `profile.html`, `selectivity.html`, `endpoint.html`, `arde.html`, `har.html` |
| [TCADBook](https://github.com/geniuskey/tcadbook) | `56d3c14f757a55caed574e720069cfdf2b7a2bf6` | `chapters/overview.html`, `implant.html`, `diffusion.html`, `topography.html`, `calibration.html`, `variability.html` |
| [YieldBook](https://github.com/geniuskey/yieldbook) | `2acd8844633274ebea91e808c4a22ed4035549b8` | `chapters/signature.html`, `commonality.html`, `statistics.html`, `models.html`, `learning.html`, `detective.html` |
| [PMICBook](https://github.com/frbread7/pmicbook) | `da37b183c559d35fcb7f6471c86c513b104a7020` | `chapters/integration.html`, `bcd.html`, `implant.html`, `anneal.html`, `etch.html`, `cmp.html`, `metal.html`, `metrology.html`, `reliability.html` |
| [WATBook](https://github.com/frbread7/watbook) | `63b0b0d14c2ea779b3314e8fef4a64a3e0c861da` | `content/en/chapters/c01`–`c10` and Korean counterparts; `docs/SCOPE_AND_OVERLAP.md`, `docs/MODELS_AND_VALIDATION.md` |

PMICBook and WATBook checkouts were clean at these revisions. The six `geniuskey` repositories use a split content/code license model in the inspected root license guides (educational content CC BY 4.0; code MIT); PMICBook documents retained/adapted ProcessBook contributions. This project takes no source text, code, illustration, question, or simulator from those books. The sources below are links for further reading and comparison. Citations do not grant reproduction rights.

## Coverage matrix

| Source | Already teaches | ProcessIntegrationBook must do instead |
|---|---|---|
| ProcessBook | `integration.html` lays out a representative CMOS flow, self-alignment and selected ordering effects; `lab.html` lets readers compose common module steps; `advanced.html` introduces HKMG/RMG, FinFET/GAA, backside power, and bonding. Separate pages teach oxidation, implants, etch, deposition, CMP, metal, metrology, and anneal. | Compare architectures and dependencies against stated constraints; make interfaces, assumptions, downstream impacts, and decision evidence explicit. Do not create another CMOS flow builder, unit-process tour, or generic thermal-budget lab. |
| DopingBook | `flow.html` follows well/channel/halo/extension/source-drain implants; `budget.html` relates accumulated thermal exposure to junction depth and sheet resistance; `diffusion.html` and `anneal.html` cover diffusion/activation. | Treat thermal history as one shared integration constraint alongside gate, isolation, contact, material, and sequence interfaces. Link for dopant physics; keep any model narrow, parameterized, assumption-visible, and not a recipe. |
| LithoBook | `transfer.html` follows resist/hard-mask/target-layer pattern transfer; `overlay.html` covers alignment, overlay measurement/correction, and edge placement; `window.html` treats focus-dose windows; `multipatterning.html` covers mask/overlay dependencies. | Explain how mask definitions, downstream transfer, CMP/topography, contacts, and layout requirements jointly constrain a technology option. Do not restate lithography theory or another focus/overlay simulator. |
| EtchBook | `selectivity.html` and `endpoint.html` cover mask/target/stop-layer budgets, endpoint, rate variation and overetch; `profile.html`, `arde.html`, and `har.html` cover etch shape and feature-depth limits. | Connect pattern transfer and etch outcomes to earlier masks/interfaces and later contacts or reliability, while linking detailed etch mechanisms. |
| TCADBook | `implant.html`, `diffusion.html`, and `topography.html` provide process/device physics; `calibration.html` covers calibration, sensitivity and DOE; `variability.html` covers device-variability models. | Teach how integration teams select model fidelity and evidence for coupled decisions; do not reproduce transport equations or present a portal simulator as calibrated TCAD. |
| YieldBook | `signature.html`, `commonality.html`, `statistics.html`, `models.html`, and `learning.html` address equipment signatures, commonality, maps, yield statistics/models and learning. | Trace a plausible integration constraint to an observable electrical/physical signature and an evidence plan. Link statistical diagnosis and yield methods rather than duplicating them. |
| PMICBook | `integration.html` explicitly describes BCD module interactions, a first-order threshold-voltage model, device-family layers and why process order matters. `bcd.html` owns the product-specific BCD context; additional chapters cover implantation/anneal, etched isolation/contact, CMP, metal, layout, characterization, and reliability. | Keep PMICBook as the BCD worked reference. Do not reproduce its BCD cross-section, device-family tutorial, Vt demonstration, PMIC application, or detailed BCD recipe. Generalize decision patterns and link to its chapters. |
| WATBook | Ten chapters own the WAT measurement-to-decision chain: monitor design, measurement conditions, extraction, uncertainty, wafer/lot context, bounded electrical hypotheses, WAT-to-EDS limits, and evidence handoff. | Refer to WATBook for measurement validity and how to test integration hypotheses. Do not repeat its monitor, wafer-map, uncertainty, WAT/EDS, or excursion-scoring labs. |

## Planned content boundary

The original book will teach five connected tasks:

1. Convert device/product targets into explicit interface requirements and integration decisions.
2. Represent module order, compatibility, thermal/material/contamination budgets, and downstream consequences as a reviewable constraint graph.
3. Compare architectural options using public cases (for example, a disclosed replacement-metal-gate CMOS platform) without presenting any commercial flow as a universal recipe.
4. Trace integration-induced variation into electrical/design/reliability outcomes, then choose measurements and experiments that discriminate among competing explanations.
5. Record assumptions, model limits, residual risk, qualification evidence, and change-control decisions.

The chapter-level plan in `docs/CONTENT_PLAN.md` follows this boundary. A section that teaches one module's standalone mechanism belongs in the specialist reference, and should be a short prerequisite/link here.

## Source and licensing boundary

The source pages were inspected to identify overlap and preserve clear ownership. Their licenses permit some reuse under conditions, but permission is not a reason to copy when original explanations are required. This book creates original prose, original diagrams, and its own tests. Every external numerical datum and technology case is cited to its public publication; no confidential process recipes, specifications, or private datasets are included. Synthetic case evidence will be labeled synthetic. No upstream cover, script, figure, paragraph, quiz, or source code is included in the deployed book.

## Audit limits

The audit sampled actual high-relevance source chapters at the pinned revisions above; it does not claim exhaustive search of every page or every semiconductor textbook. Publicly disclosed technology examples describe those papers' reported structures/results and must retain date, node/platform, and measurement context. Internal review-agent findings are not external certification or silicon validation.
