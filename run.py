import sys

from src.readme import generate_markdown_files
from src.pipeline import collect_jobs
from src.store import load_jobs, merge_jobs, save_jobs


def update():
    print("Starting job update...")

    existing_jobs = load_jobs()
    collected_jobs = collect_jobs()

    if not collected_jobs:
        print("No jobs were collected.")
        print("Existing job data and Markdown files were not changed.")
        return

    jobs = merge_jobs(collected_jobs, existing_jobs)

    save_jobs(jobs)
    generate_markdown_files(jobs)

    print(f"Saved {len(jobs)} jobs.")
    print("Generated README.md")
    print("Generated jobs/internships.md")
    print("Generated jobs/full-time.md")

    for job in jobs[:5]:
        print(
            f"{job.company} | "
            f"{job.title} | "
            f"{job.employment_type}"
        )


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