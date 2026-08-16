<!-- Generated as README.md. Edit this template, then run python run.py update. -->
# F500Tracker

[![CI](https://github.com/Tyelaman/F500Tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/Tyelaman/F500Tracker/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

F500Tracker is an automated pipeline that discovers U.S.-based internships and full-time positions from Fortune 500 career sites, enriches them with salary, skills, categories, and posting-level visa sponsorship signals, and publishes searchable job data.

Last updated: **August 16, 2026 at 07:08 UTC**

| Public metric | Count |
|---|---:|
| Tracked Fortune 500 companies | 55 |
| Internships | 41 |
| Full-time positions | 14649 |
| Total current jobs | 14690 |
| Jobs with disclosed salary | 1678 |
| Sponsorship-supported jobs | 0 |
| Jobs explicitly not offering sponsorship | 2367 |
| Jobs where sponsorship is not specified | 12323 |

[Internships](jobs/internships.md) · [Full-time roles](jobs/full-time.md) · [Searchable site](https://tyelaman.github.io/F500Tracker/) · [Public JSON](data/jobs.json)

## Features

- Greenhouse, Lever, and Workday collection behind a shared normalized job model
- U.S.-only and internship/full-time filtering across professional job families
- Conservative posting-level sponsorship classification and traceable evidence
- Employer-disclosed salary parsing and deterministic cross-discipline keywords
- Compact enrichment caching, exact deduplication, first-seen dates, and failure-safe updates
- Generated Markdown, JSON, and a dependency-free searchable static site
- Scheduled updates plus linting and mocked unit tests

## How sponsorship classification works

Sponsorship classification is based only on language in the individual job posting. `Sponsorship supported` means the posting contains sufficiently strong positive evidence. `No sponsorship for this position` means the posting explicitly rules it out. `Not specified` means the posting does not contain enough evidence to determine sponsorship availability. Employer sponsorship history is not used to classify a job, and all three statuses remain publishable.

```text
Company configuration → ATS connectors → normalize → U.S./employment filter
→ posting details → sponsorship decision → salary/keywords → enrichment cache
→ publish all eligible jobs → JSON + Markdown + static site
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
| 8 | McKesson | Workday |
| 14 | Cigna Group | Workday |
| 16 | NVIDIA | Workday |
| 19 | Centene | Workday |
| 21 | Chevron | Workday |
| 23 | General Motors | Workday |
| 26 | Fannie Mae | Workday |
| 30 | Marathon Petroleum | Workday |
| 33 | Freddie Mac | Workday |
| 34 | Humana | Workday |
| 37 | Comcast | Workday |
| 39 | Morgan Stanley | Workday |
| 41 | Dell Technologies | Workday |
| 44 | Walt Disney | Workday |
| 45 | Johnson & Johnson | Workday |
| 47 | Boeing | Workday |
| 49 | RTX | Workday |
| 52 | Lowe's | Workday |
| 55 | Sysco | Workday |
| 63 | Capital One | Workday |
| 64 | Allstate | Workday |
| 65 | Caterpillar | Workday |
| 70 | Broadcom | Workday |
| 78 | Prudential Financial | Workday |
| 83 | Cisco Systems | Workday |
| 84 | HP | Workday |
| 88 | Intel | Workday |
| 93 | USAA | Workday |
| 99 | Nike | Workday |
| 101 | GE Aerospace | Workday |
| 106 | Thermo Fisher Scientific | Workday |
| 108 | Qualcomm | Workday |
| 110 | U.S. Bancorp | Workday |
| 112 | Northrop Grumman | Workday |
| 114 | Salesforce | Workday |
| 119 | Visa | Workday |
| 125 | Micron Technology | Workday |
| 132 | Coupang | Greenhouse |
| 133 | Hewlett Packard Enterprise | Workday |
| 136 | PNC Financial Services Group | Workday |
| 139 | PayPal | Workday |
| 141 | Mastercard | Workday |
| 150 | Truist Financial | Workday |
| 160 | Applied Materials | Workday |
| 183 | 3M | Workday |
| 191 | Block | Greenhouse |
| 192 | Adobe | Workday |
| 220 | Carvana | Greenhouse |
| 294 | S&P Global | Workday |
| 329 | DoorDash | Greenhouse |
| 357 | Airbnb | Greenhouse |
| 376 | Oscar Health | Greenhouse |
| 396 | Analog Devices | Workday |
| 430 | Workday | Workday |
| 476 | Marvell Technology | Workday |

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
