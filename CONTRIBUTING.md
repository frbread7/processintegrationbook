# Contributing

ProcessIntegrationBook is an original bilingual textbook. A change should improve a reader's ability to make or evaluate a cross-module technology decision.

## Editorial contract

- Start with an engineering question involving at least two relevant interfaces or constraints.
- State which claims are **Publicly reported**, **Illustrative assumptions**, or **Engineering inferences**.
- Keep source facts separate from inference. Give public sources enough bibliographic detail to trace them.
- Prefer a concise link to an existing specialist book over repeating its device, unit-process, measurement, yield, or failure-analysis lesson.
- Never include proprietary recipes, confidential foundry data, unpublished specifications, or synthetic data that could be mistaken for observed production data.
- Translate the engineering meaning and caveats into Korean; do not translate only headings or controls.

## Quantitative content

Every numerical lab needs a model description, equations, units, validity range, assumptions, boundary and invalid-input handling, independent analytical or numerical checks where feasible, and known limitations. A JavaScript runtime check alone is not a model validation. Never describe an analytical sanity check as calibration or real-silicon validation.

The thermal lab currently carries the label **Analytically checked · model-limited**. The two other activities are qualitative.

## Local checks

~~~sh
python3 tools/build_site.py --check
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.cjs
git diff --check
~~~

Test both languages, keyboard navigation, reduced-motion and dark modes, narrow/mobile layouts, invalid numeric inputs, and desktop labs at documented sizes. Any new experiment must have a stable anchor and must be checked against its deployed route before it is registered as published in My Library.

## Scope and source boundaries

The inspected overlap is recorded in [docs/OVERLAP_AUDIT.md](docs/OVERLAP_AUDIT.md). Do not copy upstream text, code, artwork, quiz questions, or simulators. A citation is not a license grant.
