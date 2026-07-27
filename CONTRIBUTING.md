# Contributing

Contributions that improve company coverage, connectors, classification, tests, or documentation are welcome.

## Adding a company

1. Confirm that the company is currently included in the Fortune 500.
2. Identify whether its career site uses Greenhouse, Lever, or Workday.
3. Add the company to `data/companies.json`.
4. Run the tests.
5. Run a local update.
6. Verify several application links.

```bash
python -m pytest
python run.py update