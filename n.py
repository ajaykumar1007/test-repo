import re
import subprocess

# Get the name of the current branch
try:
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, check=True, text=True)
    current_branch = result.stdout.strip()
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)

# Check if the branch name matches the release branch format
if re.search(r'^\d+\.\d+\.\d+$', current_branch):
    # The code is being executed in a release branch created by the preparation script
    print(f"Current branch '{current_branch}' is a release branch.")
    match = re.search(r'^(\d+\.\d+\.\d+)$', current_branch)

if re.search(r'^\d+\.\d+\.\d+-dev$', current_branch):
    # The code is being executed in a release branch created by the preparation script
    print(f"Current branch '{current_branch}' is a release branch.")
    match = re.search(r'^(\d+\.\d+\.\d+-dev)$', current_branch)

# Get the version number from the current branch name
#match = re.search(r'^(\d+\.\d+\.\d+-dev)$', current_branch)
#print(match)
if match:
    version = match.group(1)
    print(f"Version number is '{version}'.")

    # Check if the release tag with that version already exists
    try:
        result = subprocess.run(['git', 'tag'], capture_output=True, check=True, text=True)
        tags = result.stdout.strip().split('\n')
        if f'release-v{version}' in tags:
            print(f"Release tag 'release-v{version}' already exists.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit(1)

# Push the current branch to the release branch
try:
    subprocess.run(['git', 'push', 'origin', current_branch], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)

tag_name = f'release-v{version}'

# Create the tag and push it to the remote repository
try:
    subprocess.run(['git', 'tag', tag_name], check=True)
    subprocess.run(['git', 'push', 'origin', tag_name], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    exit(1)

