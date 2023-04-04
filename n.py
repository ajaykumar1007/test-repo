import re
import subprocess

# Get the name of the current branch
current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')

# Check if the branch name matches the release branch format
if re.match(r'^release-v\d+\.\d+\.\d+$', current_branch):
    # The code is being executed in a release branch created by the preparation script
    ...

# Get the version number from the current branch name
match = re.match(r'^release-v(\d+\.\d+\.\d+)$', current_branch)
if match:
    version = match.group(1)
    print(match.group(1))
    
    # Check if the release tag with that version already exists
    tags = subprocess.check_output(['git', 'tag']).strip().decode('utf-8').split('\n')
    if f'release-v{version}' in tags:
        # The release tag already exists
        ...

# Push the current branch to the release branch
subprocess.check_call(['git', 'push', 'origin', current_branch])

# Determine the tag name based on the current branch name
if current_branch.endswith('-dev'):
    tag_name = f'release-{version}-dev'
else:
    tag_name = f'release-{version}'

# Create the tag and push it to the remote repository
subprocess.check_call(['git', 'tag', tag_name])
subprocess.check_call(['git', 'push', 'origin', tag_name])

