import os
import argparse

# File path
file_path = "release_info.txt"

os.system(f"git fetch --all")
version = os.popen("git branch -a --sort=-version:refname| awk -v FS='/' '{print $3}'|awk '/[0-9]/'|sort|tail -1").read().strip()

if not version:
    version = '0.0.0'
    with open(file_path, "w") as f:
        f.write(f"VERSION: {version}\n")

# Get the commit ID, last commit hash, source branch, and commit date
COMMIT_ID = os.popen('git rev-parse --short HEAD').read().strip()
LAST_COMMIT_HASH = os.popen('git rev-parse HEAD').read().strip()
SOURCE_BRANCH = os.popen('git branch --show-current').read().strip()
COMMIT_DATE = os.popen("git log -1 --stat | grep -i date | cut -d' ' -f5-").read().strip()

# Define a function tlshat writes a new branch_details.txt file with the specified version and commit information
def write_file(version, commit_id, last_commit_hash, source_branch, commit_date):
    with open("release_info.txt", "w") as f:
        f.write(f"VERSION: {version}\nCOMMIT_ID: {commit_id}\nCOMMIT_HASH: {last_commit_hash}\nSOURCE_BRANCH: {source_branch}\nCOMMIT_DATE: {commit_date}\n")

# Define functions for incrementing the version number
def increment_version(version):
    parts = version.replace("-dev","").split('.')
    parts[2] = str(int(parts[2]) + 1)
    return '.'.join(parts)

def increment_minor(version):
    parts = version.replace("-dev","").split('.')
    parts[1] = str(int(parts[1]) + 1)
    parts[2] = "0"
    return '.'.join(parts)

def increment_major(version):
    parts = version.replace("-dev","").split('.')
    parts[0] = str(int(parts[0]) + 1)
    parts[1] = "0"
    parts[2] = "0"
    return '.'.join(parts)

# Define functions for bumping the version number
def patch(flag):
    new_version = increment_version(version) + flag
    output = os.popen('git status').read()
    if 'Changes not staged for commit' in output  or 'Untracked files' in output:
        os.system(f"git status > gitstatus")
        os.system(f"git checkout -b {new_version}")
        os.system(f"git add .")
        os.system(f'git commit -m "patch {new_version}"')
        COMMIT_ID = os.popen('git rev-parse --short HEAD').read().strip()
        LAST_COMMIT_HASH = os.popen('git rev-parse HEAD').read().strip()
        SOURCE_BRANCH = os.popen('git branch --show-current').read().strip()
        COMMIT_DATE = os.popen("git log -1 --stat | grep -i date | cut -d' ' -f4-").read().strip()
        write_file(new_version, COMMIT_ID, LAST_COMMIT_HASH, SOURCE_BRANCH, COMMIT_DATE)
        os.system(f"git add .")
        os.system(f'git commit -m "file update {new_version}"')

def minor(flag):
    new_version = increment_minor(version) + flag
    output = os.popen('git status').read()
    if 'Changes not staged for commit' in output or 'Untracked files' in output:
        os.system(f"git status > gitstatus")
        os.system(f"git checkout -b {new_version}")
        os.system(f"git add .")
        os.system(f'git commit -m "minor {new_version}"')
        COMMIT_ID = os.popen('git rev-parse --short HEAD').read().strip()
        LAST_COMMIT_HASH = os.popen('git rev-parse HEAD').read().strip()
        SOURCE_BRANCH = os.popen('git branch --show-current').read().strip()
        COMMIT_DATE = os.popen("git log -1 --stat | grep -i date | cut -d' ' -f4-").read().strip()
        write_file(new_version, COMMIT_ID, LAST_COMMIT_HASH, SOURCE_BRANCH, COMMIT_DATE)
        os.system(f"git add .")
        os.system(f'git commit -m "file update {new_version}"')
    
def major(flag):
    new_version = increment_major(version) + flag
    output = os.popen('git status').read()
    if 'Changes not staged for commit' in output or 'Untracked files' in output:
        os.system(f"git status >gitstatus")
        os.system(f"git checkout -b {new_version} ")
        os.system(f"git add .")
        os.system(f'git commit -m "major {new_version} "')
        COMMIT_ID = os.popen('git rev-parse --short HEAD').read().strip()
        LAST_COMMIT_HASH = os.popen('git rev-parse HEAD').read().strip()
        SOURCE_BRANCH = os.popen('git branch --show-current').read().strip()
        COMMIT_DATE = os.popen("git log -1 --stat | grep -i date | cut -d' ' -f4-").read().strip()
        write_file(new_version, COMMIT_ID, LAST_COMMIT_HASH, SOURCE_BRANCH, COMMIT_DATE)
        os.system(f"git add .")
        os.system(f'git commit -m "file update {new_version} "') 


# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--dev-build", help="Appending -dev to the release branch name", action="store_true")
parser.add_argument("--bump-major-version", help="Bump major version", action="store_true")
parser.add_argument("--bump-minor-version", help="Bump minor version", action="store_true")
parser.add_argument("--bump-patch-version", help="Bump patch version", action="store_true")


args = parser.parse_args()

# Call the appropriate function based on the command-line arguments
if args.dev_build:
    if args.bump_major_version and args.bump_minor_version:
        print("Only one of --bump-major-version or --bump-minor-version or --bump-patch-version can be specified.")
    elif args.bump_major_version:
        major("-dev")
    elif args.bump_minor_version:
        minor("-dev")
    elif args.bump_patch_version:
        patch("-dev")
else:
    if args.bump_major_version and args.bump_minor_version:
        print("Only one of --bump-major-version or --bump-minor-version or --bump-patch-version can be specified.")
    elif args.bump_major_version:
        major("")
    elif args.bump_minor_version:
        minor("")
    elif args.bump_patch_version:
        patch("")
