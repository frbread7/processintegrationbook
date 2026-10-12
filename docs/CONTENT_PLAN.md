# Content plan and editorial boundary

## Reader and outcome

The intended readers are semiconductor process-integration, device, technology-development, and yield engineers, with advanced graduate readers as a secondary audience. Readers are expected to know basic device physics and the names/purposes of lithography, etch, deposition, implant, anneal, isolation, contacts, and interconnect.

After the book, a reader should be able to turn a device/product target into an explicit integration problem; draw process dependencies and interface assumptions; compare at least two candidate architectures; identify the evidence needed to test a cross-module hypothesis; and document why a choice is accepted, rejected, or still uncertain.

The book teaches decisions across modules. It assumes, links, or briefly refreshes standalone module physics. It is not a process recipe, process-flow survey, TCAD solver, WAT manual, yield-analysis textbook, or product-specific BCD tutorial. `docs/OVERLAP_AUDIT.md` records the inspected coverage and source revisions.

## Chapter sequence

| No. | Stable ID | English title | Korean title | Engineering question |
|---:|---|---|---|---|
| 1 | `c01-integration-as-decision` | Integration as a technology decision | 기술 의사결정으로서의 공정 통합 | How do requirements, architecture, constraints, evidence, and residual risk form one reviewable decision? |
| 2 | `c02-requirements-to-architecture` | From requirements to process architecture | 요구사항에서 공정 아키텍처까지 | How are device portfolios and system targets allocated into a feasible process architecture? |
| 3 | `c03-sequence-interface-contracts` | Sequence dependencies and interface contracts | 공정 순서 의존성과 인터페이스 계약 | Which orderings, material states, and preconditions make two individually sound modules incompatible? |
| 4 | `c04-isolation-substrate-choices` | Isolation and substrate as shared interfaces | 공통 인터페이스로서의 절연과 기판 | How do substrate and isolation choices constrain neighboring device modules, parasitics, area, and later processing? |
| 5 | `c05-gate-stack-architecture` | Gate-stack architecture and process order | 게이트 스택 아키텍처와 공정 순서 | What integration trade-offs distinguish gate-first and replacement-metal-gate sequences? |
| 6 | `c06-junction-thermal-history` | Junction evolution under a shared thermal history | 누적 열 이력에 따른 접합 변화 | How can several thermal steps be combined in a deliberately bounded diffusion estimate, and what does it omit? |
| 7 | `c07-pattern-transfer-chain` | Pattern transfer across lithography, etch, and planarization | 리소그래피·식각·평탄화 간 패턴 전사 | How do pattern definition, transfer, overlay, and planarization jointly constrain downstream features? |
| 8 | `c08-contact-mol-interface` | The contact and middle-of-line interface | 콘택트와 MOL 인터페이스 | How do source/drain, silicide or contact materials, cleans, and local routing compete for a low-resistance reliable interface? |
| 9 | `c09-beol-compatibility` | Back-end integration and material compatibility | 배선 공정 통합과 재료 호환성 | How do conductor/barrier/dielectric choices, thermal history, plasma, and topography affect earlier devices and later interconnect? |
| 10 | `c10-variation-propagation` | How integration choices propagate variation | 통합 선택에 따른 변동 전파 | How does a variation source cross module boundaries before becoming an electrical or product-level observation? |
| 11 | `c11-design-technology-cooptimization` | Design-technology co-optimization | 설계-기술 공동 최적화 | How are device, layout, patterning, process-window, and circuit targets balanced together? |
| 12 | `c12-integration-learning-qualification` | Learning, qualification, and controlled change | 학습·품질 인증·변경 관리 | What experiment and evidence gate can discriminate an integration hypothesis and qualify a controlled change? |
| 13 | `c13-public-platform-case` | Reading a disclosed platform as an integration case | 공개 플랫폼을 통합 사례로 읽기 | How does a disclosed high-k-first/metal-gate-last flow connect workfunction and thermal-budget constraints, and what evidence does that case not establish? |

## Editorial requirements for every chapter

Each English/Korean pair must preserve the same concepts, caveats, and labels, while using natural engineering language in each language. A chapter needs a concrete decision question, stated learning objectives, a cross-module explanation, assumptions/limits where equations appear, at least one worked engineering example, a short knowledge check with an explanation, and traceable reading links. A chapter should connect an upstream choice to one or more downstream consequences, not merely inventory modules.

Chapter topic metadata follows My Library's current Book Factory contract, where `topics` is a list of strings. Each topic is stored as `English / 한국어`; the site build validates this form, displays only the current locale, and keeps both terms searchable. This preserves the central JSON schema without adding unsupported manifest fields.

Use three evidence labels consistently:

- **Publicly reported:** a directly attributed result or implementation detail from a public paper/document, with its date/platform context.
- **Illustrative assumption:** a clearly marked teaching scenario, invented value, or simplified relationship. Do not imply it describes a foundry or real production flow.
- **Engineering inference:** a reasoned consequence that is not itself the cited paper's explicit claim; label it as an inference and state what measurement/model would test it.

Do not equate an internal reviewer-agent pass with professional certification, TCAD calibration, fab acceptance, or silicon validation. Never give proprietary mask sequences, process recipes, or commercial specifications.

## Interactive laboratory scope

1. **Process dependency explorer:** qualitative, evidence-labeled interface graph. It teaches declared precedence and compatibility relationships; it has no physical-response engine and cannot validate a recipe.
2. **Thermal-history/junction experiment:** a one-dimensional, constant-diffusivity Gaussian-profile calculation using an explicit Arrhenius parameter set. Its default is the classical dilute equilibrium boron-in-silicon parameterization cited on the page. Users can add/remove thermal holds and see the modeled profile broadening and threshold crossing. The interface must state that it omits implant damage/TED, concentration and charge-state effects, activation/clustering, oxidation injection, segregation/interface motion, ramps unless discretized, and real process calibration. Results are analytically checked and independently reimplemented in Python; they are not externally validated or silicon validated.
3. **Integration review challenge:** a qualitative public-case or labeled synthetic evidence ledger. Learners choose which constraint or evidence gap to investigate next; feedback is explanatory and ordinal only. It must not display fabricated probabilities or claim automated root-cause inference.

Do not add extra numerical “physics” merely to make the lab look richer. The simulator labels should say `Analytically checked · model-limited` until independent implementation and boundary tests pass. There is no basis here for an `Externally reference-checked` or `silicon validated` label.

## Citation verification evidence

The citation-by-citation metadata and claim-support audit is recorded in [`CITATION_AUDIT.md`](CITATION_AUDIT.md). It maps checked claims to accessible papers, source locations, and limits on inference. For the Arrhenius pair, Esser et al. print the values and cite Sze's edited *VLSI Technology* (1983); Mostafa and Medraj also print them while citing W. J. Scotten's *Diffusion in Silicon* (2000). Neither historical page/table has been independently verified, so the claim is documented as supported by accessible reports while original provenance remains unresolved. Sze and Ng (2007) is retained as general background only. The audit is not silicon validation.

The sources are not blanket support for every chapter claim. Synthetic scenarios and engineering inferences are identified as such. A DOI is a bibliography pointer, not permission to reproduce copyrighted figures or tables. The audit distinguishes a public paper's reported claim from this project's interpretation and does not treat reviewer-agent approval as external professional or laboratory validation.
