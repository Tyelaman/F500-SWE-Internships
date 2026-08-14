import sys

from src.pipeline import collect_jobs
from src.readme import generate_markdown_files
from src.sponsorship import SUPPORTS_H1B
from src.store import load_jobs, merge_jobs, save_jobs


def update():
    print("Starting job update...")

    existing_jobs = load_jobs()

    (
        collected_jobs,
        successful_companies,
        failed_companies,
    ) = collect_jobs()

    if not successful_companies:
        print("Every supported company fetch failed.")
        print("Existing files were not changed.")
        return

    jobs = merge_jobs(
        collected_jobs,
        existing_jobs,
        failed_companies,
    )
    jobs = [job for job in jobs if job.h1b_status == SUPPORTS_H1B]

    save_jobs(jobs)
    generate_markdown_files(jobs)

    print(f"Saved {len(jobs)} jobs.")
    print(f"Companies attempted: {len(successful_companies) + len(failed_companies)}")
    print(f"Companies successful: {len(successful_companies)}")
    print(f"Companies failed: {len(failed_companies)}")
    print(f"Sponsored internships: {sum(job.employment_type == 'internship' for job in jobs)}")
    print(f"Sponsored full-time jobs: {sum(job.employment_type == 'full-time' for job in jobs)}")
    print(f"Total published jobs: {len(jobs)}")
    print(f"Jobs with salary information: {sum(job.salary_min is not None for job in jobs)}")

    if failed_companies:
        failed_names = ", ".join(sorted(failed_companies))
        print(f"Preserved old jobs for: {failed_names}")

    print("Generated README.md")
    print("Generated jobs/internships.md")
    print("Generated jobs/full-time.md")

    for job in jobs[:5]:
        print(f"{job.company} | {job.title} | {job.employment_type}")


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
