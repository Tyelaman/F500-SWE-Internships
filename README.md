<!-- Generated as README.md. Edit this template, then run python run.py update. -->
# F500Tracker

[![CI](https://github.com/Tyelaman/F500Tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Tyelaman/F500Tracker/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

F500Tracker is an automated Fortune 500 job aggregation and enrichment pipeline that discovers U.S.-based internships and full-time opportunities with explicit H-1B/employment visa sponsorship support. It enriches qualifying postings with employer-disclosed salary information and job-relevant keywords, then publishes searchable Markdown, JSON, and a lightweight web interface.

Last updated: **August 14, 2026 at 22:43 UTC**

| Public metric | Count |
|---|---:|
| Tracked Fortune 500 companies | 20 |
| H-1B-supporting internships | 0 |
| H-1B-supporting full-time positions | 0 |
| Total sponsorship-supported positions | 0 |
| Positions with disclosed salary | 0 |

[Internships](jobs/internships.md) · [Full-time roles](jobs/full-time.md) · [Searchable site](https://tyelaman.github.io/F500Tracker/) · [Public JSON](data/jobs.json)

## Features

- Greenhouse, Lever, and Workday collection behind a shared normalized job model
- U.S.-only and internship/full-time filtering across professional job families
- Conservative posting-level sponsorship classification and traceable evidence
- Employer-disclosed salary parsing and deterministic cross-discipline keywords
- Compact enrichment caching, exact deduplication, first-seen dates, and failure-safe updates
- Generated Markdown, JSON, and a dependency-free searchable static site
- Scheduled updates plus linting and mocked unit tests

## How sponsorship filtering works

F500Tracker evaluates wording in each individual public posting. Explicit H-1B availability or strong role-specific U.S. employment-based immigration sponsorship qualifies. Explicit restrictions override positive-looking text. Missing, vague, conflicting, OPT/CPT-only, or inaccessible language becomes `unknown` and is excluded. Historical employer reputation never qualifies a posting.

```text
Company configuration → ATS connectors → normalize → U.S./employment filter
→ posting details → sponsorship decision → salary/keywords → enrichment cache
→ sponsored-only publication → JSON + Markdown + static site
```

## Supported ATS platforms

| ATS | Identifier |
|---|---|
| Greenhouse | Board token |
| Lever | Lever site name |
| Workday | Complete public careers URL |

## Tracked companies

| Fortune rank | Company | ATS |
|---:|---|---|
| 16 | NVIDIA | Workday |
| 41 | Dell Technologies | Workday |
| 47 | Boeing | Workday |
| 63 | Capital One | Workday |
| 84 | HP | Workday |
| 88 | Intel | Workday |
| 108 | Qualcomm | Workday |
| 112 | Northrop Grumman | Workday |
| 114 | Salesforce | Workday |
| 119 | Visa | Workday |
| 125 | Micron Technology | Workday |
| 132 | Coupang | Greenhouse |
| 139 | PayPal | Workday |
| 141 | Mastercard | Workday |
| 191 | Block | Greenhouse |
| 192 | Adobe | Workday |
| 294 | S&P Global | Workday |
| 329 | DoorDash | Greenhouse |
| 357 | Airbnb | Greenhouse |
| 430 | Workday | Workday |

Ranks and verified ATS identifiers are maintained in [`data/companies.json`](data/companies.json).

## Project structure

```text
data/             company config, public jobs, compact enrichment cache
docs/             static search interface and compact site JSON
jobs/             generated internship and full-time Markdown
src/connectors/   Greenhouse, Lever, and Workday adapters
src/              classifiers, enrichment, pipeline, storage, generators
tests/            deterministic unit and integration-style tests
run.py            command-line updater
```

## Local development

```bash
git clone https://github.com/Tyelaman/F500Tracker.git
cd F500Tracker
python -m venv .venv
# activate the environment, then:
python -m pip install -r requirements-dev.txt
python -m pytest
ruff check .
ruff format --check .
python run.py update
```

To add a company, verify its current Fortune 500 rank and official ATS identifier, add the four required fields (`name`, `fortune_rank`, `source`, `identifier`) to `data/companies.json`, run validation/tests and a local update, then inspect application links. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Automation and generated files

CI runs on pushes and pull requests. The update workflow runs approximately every six hours, serializes updates, tests before collection, safely rebases, and commits only generated artifacts. Do not hand-edit `README.md`, `data/jobs.json`, `data/enrichment_cache.json`, `docs/jobs.json`, or `jobs/*.md`; change their sources and rerun the updater.

## Enrichment and limitations

Descriptions are used transiently and are not stored wholesale. The cache keeps only a posting identity/update marker, sponsorship result/evidence, salary fields, keywords, and enrichment time; unchanged postings reuse it, while postings without update timestamps expire after seven days. Salary is only employer-disclosed compensation and may be absent. Heuristics favor false negatives, postings and ATS formats can change, and eligibility can depend on applicant circumstances.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, generated-file policy, testing expectations, and the pull-request checklist.

## Disclaimer

F500Tracker is not legal or immigration advice and does not guarantee sponsorship. Verify the current posting and your eligibility directly with the employer.

## License

[MIT](LICENSE)
