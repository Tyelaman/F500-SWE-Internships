# Contributing

Create and activate a Python 3.12 virtual environment, then run `python -m pip install -r requirements-dev.txt`. Before a pull request, run `python -m pytest`, `ruff check .`, `ruff format --check .`, and—when relevant—`python run.py update`.

## Changes

- Companies: verify the current Fortune 500 rank, official careers site, ATS, and identifier; add all four required fields to `data/companies.json`; run tests/update and inspect several application links.
- Connectors: keep ATS-specific fetching/detail logic inside `src/connectors`, normalize to `Job`, use the shared HTTP client, and add mocked listing/detail tests.
- Classifiers/enrichment: keep rules deterministic and conservative. Add positive, negative, ambiguous, boundary, and regression tests. Company reputation is never sponsorship evidence.
- Generated files: edit source/template/configuration files, then regenerate `README.md`, `data/jobs.json`, `data/enrichment_cache.json`, `docs/jobs.json`, and `jobs/*.md`. Do not hand-maintain generated counts.

Never add credentials, private applicant information, invented ranks/identifiers, or non-public data.

## Pull-request checklist

- [ ] Scope is focused and documented.
- [ ] Tests and both Ruff commands pass.
- [ ] New network behavior is mocked in unit tests.
- [ ] Company configuration validates and application links were checked.
- [ ] Public artifacts contain only `supports_h1b` U.S. internship/full-time jobs.
- [ ] Generated artifacts were refreshed when their sources changed.
