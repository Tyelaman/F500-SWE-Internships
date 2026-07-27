<!--
README.md is generated from this template.
Edit README_TEMPLATE.md instead of editing README.md directly.
-->

# Fortune 500 Job Tracker

[![Update Fortune 500 jobs](https://github.com/Tyelaman/F500-SWE-Internships/actions/workflows/update.yml/badge.svg)](https://github.com/Tyelaman/F500-SWE-Internships/actions/workflows/update.yml)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An automated Python pipeline that collects open positions from Fortune 500 company career sites, normalizes them into a shared format, classifies them by employment type and job category, and publishes searchable Markdown job lists.

**Last updated:** July 27, 2026 at 15:15 UTC

## Current listings

| Metric | Count |
|---|---:|
| Tracked companies | 12 |
| Internships | 2 |
| Full-time positions | 4220 |
| Total positions | 4222 |

### Browse the data

- [Internship listings](jobs/internships.md)
- [Full-time listings](jobs/full-time.md)
- [Machine-readable job data](data/jobs.json)
- [Tracked company configuration](data/companies.json)

## Features

- Collects jobs from multiple applicant-tracking systems
- Supports Greenhouse, Lever, and Workday career sites
- Normalizes platform-specific postings into one shared job model
- Separates internships from full-time positions
- Excludes part-time, contract, temporary, seasonal, and freelance roles
- Classifies jobs into categories such as Software & IT, Data & AI, Engineering, Finance, and Operations
- Removes duplicate postings using company, source, and external job identifiers
- Preserves existing listings when an individual company request fails
- Records when each posting was first discovered
- Produces both Markdown and JSON output
- Runs automatically through GitHub Actions
- Includes automated tests for connectors, pagination, classification, and deduplication

## How it works

```text
data/companies.json
        |
        v
Connector registry
        |
        +-- Greenhouse connector
        +-- Lever connector
        +-- Workday connector
        |
        v
Platform-specific normalization
        |
        v
Employment and category classification
        |
        v
Deduplication and safe merge
        |
        +-- data/jobs.json
        +-- jobs/internships.md
        +-- jobs/full-time.md
        +-- README.md
```

Each connector retrieves jobs from one hiring platform and converts the results into the shared `Job` model. The pipeline then classifies, deduplicates, merges, and writes the final output files.

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
| 63 | Capital One | Workday |
| 112 | Northrop Grumman | Workday |
| 114 | Salesforce | Workday |
| 132 | Coupang | Greenhouse |
| 141 | Mastercard | Workday |
| 191 | Block | Greenhouse |
| 192 | Adobe | Workday |
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

### 5. Update the listings

```bash
python run.py update
```

The command retrieves jobs, updates `data/jobs.json`, and regenerates the Markdown files.

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

- Employment type and category classification are based on job titles and available metadata.
- Some career platforms expose more information than others.
- Public career-site structures may change without notice.
- Fortune rankings and company identifiers must be updated manually.
- A listing may close between an automated update and an application attempt.
- The project currently tracks open positions rather than maintaining a historical archive of closed listings.

## Disclaimer

This project is not affiliated with Fortune, Greenhouse, Lever, Workday, or any tracked company. Listings are collected from public company hiring platforms. Always verify a position on the employer’s official career site before applying.

## License

This project is available under the [MIT License](LICENSE).