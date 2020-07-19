import os
import random
import subprocess
from datetime import datetime, timedelta

commits_per_year = {
    2019: 453,
    2020: 689,
    2021: 1117,
    2022: 462,
    2023: 1371,
    2024: 1847,
    2025: 2749,
}

FILENAME = "commit_activity_log.txt"

def random_date(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31, 23, 59, 59)
    time_between_dates = end_date - start_date
    random_seconds = random.randrange(int(time_between_dates.total_seconds()))
    return start_date + timedelta(seconds=random_seconds)

def main():
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        subprocess.run(["git", "init"], check=True)
        
    dates = []
    print("Generating random dates for commits...")
    for year, count in commits_per_year.items():
        for _ in range(count):
            dates.append(random_date(year))
            
    dates.sort()
    total_commits = len(dates)
    print(f"Total commits to generate: {total_commits}")
    
    with open(FILENAME, "w") as f:
        f.write("Git Commit History Start\n")
    subprocess.run(["git", "add", FILENAME], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=False)
    subprocess.run(["git", "branch", "-M", "main"], check=True)

    for i, dt in enumerate(dates, 1):
        date_str = dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        with open(FILENAME, "a") as f:
            f.write(f"Commit on {date_str}\n")
            
        subprocess.run(["git", "add", FILENAME], check=True)
        message = f"Activity commit for {dt.strftime('%Y-%m-%d')}"
        
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = date_str
        env['GIT_COMMITTER_DATE'] = date_str
        
        subprocess.run(
            ["git", "commit", "-q", "-m", message],
            env=env
        )
        
        if i % 1000 == 0:
            print(f"Progress: {i} / {total_commits} commits generated...")

    print("Finished generating commits.")

if __name__ == "__main__":
    main()
