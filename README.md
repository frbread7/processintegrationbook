# ProcessIntegrationBook

**Advanced Process Integration & Technology Co-Optimization**
An independent English–Korean engineering textbook about cross-module constraints, process sequence, technology trade-offs, and evidence-led decisions.

ProcessIntegrationBook focuses on the decisions that connect process modules. It is not a process recipe, a unit-process survey, a TCAD solver, a wafer-measurement manual, or a yield-analysis reference. It links readers to specialist sources rather than duplicating their material.

## Read the book

- Production candidate: <https://frbread7.github.io/processintegrationbook/>
- Korean edition: <https://frbread7.github.io/processintegrationbook/ko/>
- Interactive laboratory: <https://frbread7.github.io/processintegrationbook/lab.html>
- Scope and overlap audit: [docs/OVERLAP_AUDIT.md](docs/OVERLAP_AUDIT.md)

The website is built from the site directory. Chapter source fragments are in the English and Korean content directories; the library manifest is the book's catalog contract. My Library registers this repository and links to it. It does not copy or redeploy the textbook.

## Develop locally

Requirements: Python 3.11 or newer and Node.js 20 or newer. No runtime package dependencies are required.

~~~sh
python3 tools/build_site.py
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/*.test.cjs
python3 -m http.server 8000 --directory site
~~~

Then open <http://localhost:8000/>. Check both languages, chapter links, theme toggle, chapter search, knowledge checks, and laboratory controls at desktop and narrow mobile sizes.

## Technical evidence

The thermal-history laboratory is a one-dimensional dilute, constant-diffusivity educational model. Its equations, assumptions, input limits, analytical reference case, independently evaluated Python results, and explicit non-validation statements are documented in [docs/MODELS_AND_VALIDATION.md](docs/MODELS_AND_VALIDATION.md). It is analytically checked and model-limited; it is not calibrated against a foundry flow or validated against real silicon.

The dependency explorer and case challenge are qualitative learning activities. Neither calculates a recipe, risk probability, process capability, or root cause.

## Book Factory registration

Use the My Library Book Factory contract. The starter schema and registration commands are documented in the central repository's [Book Factory guide](https://github.com/frbread7/books/blob/main/docs/BOOK_FACTORY.md). This repository's manifest remains in-progress until the release, deployment, content, route, and experiment evidence gates succeed.

## Licensing and attribution

Original educational text, translations, artwork, and synthetic examples are licensed under CC BY 4.0. Original software is licensed under MIT. Referenced papers and independent textbooks retain their respective owners and terms. Read [LICENSE.md](LICENSE.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for editorial, technical, and verification rules.
