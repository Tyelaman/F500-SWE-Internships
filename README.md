<!--
README.md is generated from this template.
Edit README_TEMPLATE.md instead of editing README.md directly.
-->

# Fortune 500 Job Tracker

[![Update Fortune 500 jobs](https://github.com/Tyelaman/F500-SWE-Internships/actions/workflows/update.yml/badge.svg)](https://github.com/Tyelaman/F500-SWE-Internships/actions/workflows/update.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An automated Python pipeline that collects United States-based positions from Fortune 500 company career sites, normalizes postings from multiple hiring platforms, classifies them by employment type and job category, and publishes continuously updated Markdown and JSON job listings.

**Last updated:** August 05, 2026 at 14:37 UTC

## Current listings

| Metric | Count |
|---|---:|
| Tracked companies | 20 |
| Internships | 11 |
| Full-time positions | 5011 |
| Total positions | 5022 |

### Browse the listings

- [Internship listings](jobs/internships.md)
- [Full-time listings](jobs/full-time.md)
- [Machine-readable job data](data/jobs.json)
- [Tracked company configuration](data/companies.json)

The internship and full-time pages include clickable category navigation for Software & IT, Data & AI, Engineering, Product & Design, Finance, Operations, and other job families.

## Features

- Collects public jobs from Fortune 500 company career sites
- Supports Greenhouse, Lever, and Workday
- Normalizes different hiring-platform responses into one shared `Job` model
- Filters listings to United States locations
- Separates internships from full-time positions
- Excludes part-time, contract, temporary, seasonal, and freelance roles
- Classifies jobs into categories such as Software & IT, Data & AI, Engineering, Finance, and Operations
- Generates clickable category navigation in each Markdown job list
- Removes duplicate postings using company, source, and external job identifiers
- Preserves previous listings when an individual company request temporarily fails
- Records when each job was first discovered
- Publishes Markdown listings and machine-readable JSON data
- Runs automatically every six hours with GitHub Actions
- Includes automated tests for connectors, pagination, classification, location filtering, Markdown generation, and deduplication

## How it works

```text
data/companies.json
        |
        v
Connector registry
        |
        +-- Greenhouse
        +-- Lever
        +-- Workday
        |
        v
Platform-specific normalization
        |
        v
Employment classification
        |
        v
United States location filtering
        |
        v
Job-category classification
        |
        v
Deduplication and failure-safe merge
        |
        +-- data/jobs.json
        +-- jobs/internships.md
        +-- jobs/full-time.md
        +-- README.md

## Supported hiring platforms

| Source | Company identifier |
|---|---|
| Greenhouse | Company board token |
| Lever | Lever site name |
| Workday | Complete public Workday careers URL |

## Tracked companies

| Fortune rank | Company | Source |
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

Company rankings and career-site identifiers are maintained in [`data/companies.json`](data/companies.json).

## Project structure

```text
.
├── .github/
│   └── workflows/
│       └── update.yml
├── data/
│   ├── companies.json
│   └── jobs.json
├── jobs/
│   ├── internships.md
│   └── full-time.md
├── src/
│   ├── connectors/
│   │   ├── greenhouse.py
│   │   ├── lever.py
│   │   └── workday.py
│   ├── categories.py
│   ├── classify.py
│   ├── companies.py
│   ├── models.py
│   ├── pipeline.py
│   ├── readme.py
│   └── store.py
├── tests/
├── README_TEMPLATE.md
├── requirements.txt
└── run.py
```

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/Tyelaman/F500-SWE-Internships.git
cd F500-SWE-Internships
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the tests

```bash
python -m pytest
```


Be careful: because the outer section contains a code block, copy it directly into the Markdown file rather than placing it inside another code block.

## 5. Update the project structure

Add `locations.py`:

```text
├── src/
│   ├── connectors/
│   │   ├── greenhouse.py
│   │   ├── lever.py
│   │   └── workday.py
│   ├── categories.py
│   ├── classify.py
│   ├── companies.py
│   ├── locations.py
│   ├── models.py
│   ├── pipeline.py
│   ├── readme.py
│   └── store.py

## Adding a company

Add an object to `data/companies.json`.

### Greenhouse

```json
{
  "name": "Example Company",
  "fortune_rank": 100,
  "source": "greenhouse",
  "identifier": "example-board-token"
}
```

### Lever

```json
{
  "name": "Example Company",
  "fortune_rank": 100,
  "source": "lever",
  "identifier": "example-site-name"
}
```

### Workday

```json
{
  "name": "Example Company",
  "fortune_rank": 100,
  "source": "workday",
  "identifier": "https://example.wd5.myworkdayjobs.com/en-US/Careers"
}
```

After editing the configuration, run:

```bash
python -m pytest
python run.py update
```

Verify that the company appears in `data/jobs.json` and that several generated application links work.

## Automation

The GitHub Actions workflow:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs the test suite
5. retrieves current job postings
6. Regenerates the output files
7. Commits changes when the listings have changed

The workflow runs every six hours and can also be started manually.

## Generated files

These files are generated by the pipeline:

- `README.md`
- `data/jobs.json`
- `jobs/internships.md`
- `jobs/full-time.md`

Do not permanently edit these files by hand. Update the source code, company configuration, or `README_TEMPLATE.md`, then run `python run.py update`.

## Known limitations

- Employment type and job category are inferred from titles and available posting metadata.
- Location formats differ between hiring platforms.
- Country-unspecified remote positions are excluded because they cannot be verified as United States-based.
- A posting containing both U.S. and international locations is included when at least one recognized U.S. location is present.
- Public career-site endpoints and identifiers may change without notice.
- Fortune rankings and company configurations must be maintained manually.
- Job postings may close between automated updates.
- The tracker stores current open positions rather than a historical archive of closed jobs.

## Disclaimer

This project is not affiliated with Fortune, Greenhouse, Lever, Workday, or any tracked company. Listings are collected from public company hiring platforms. Always verify a position on the employer’s official career site before applying.

## License

This project is available under the [MIT License](LICENSE).