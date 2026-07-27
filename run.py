import sys

from src.readme import generate_markdown_files
from src.pipeline import collect_jobs
from src.store import load_jobs, save_jobs


def update():
    print("Starting job update...")

    jobs = collect_jobs()

    save_jobs(jobs)
    generate_markdown_files(jobs)

    saved_jobs = load_jobs()

    print(f"Saved {len(saved_jobs)} jobs.")
    print("Generated README.md")
    print("Generated jobs/internships.md")
    print("Generated jobs/full-time.md")

    for job in saved_jobs[:5]:
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