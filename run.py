import sys
from src.models import Job

def update():
    print("Starting internship update...")

    sample_job = Job(
        company="Walmart",
        title="Software Engineering Intern",
        location="Bentonville, AR",
        url="https://example.com/apply",
        source="greenhouse",
        external_id="12345",
    )

    print(sample_job)


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py update")
        return

    command = sys.argv[1]

    if command == "update":
        update()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()