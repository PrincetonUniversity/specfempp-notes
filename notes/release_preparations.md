# Release Preparations

## Create a draft release on GitHub. 

- Go to the "Releases" section of the repository.
- Click on "Draft a new release".
- Set the tag version (e.g., `v1.0.0`).
- Add a title and description for the release.
- Automatically generate release notes by selecting the "Generate release
  notes" option. We implemented the `./github/release.yaml` and are tagging
  each PR with a supported label.
- Save the draft.

## Create TL;DR

- Manually create a TL;DR section for the release notes highlighting with bullet
  points the most important changes, features, and fixes.

## Create a TL;DR explanations

For some releases you will want to add some examples (e.g, GIF of a simulation,
etc.) and explain the most important changes in more detail. You can only really
do this manually.

## Create Statistics sections

Total commits between the last release and the current one, total number of
```bash
git log --oneline <previous release tag>..<target branch> | wc -l
```

An actual command would look like this for the `devel` branch:
```bash
git log --oneline v0.3.0..devel | wc -l
```

To get the total number of PRs going into the release, we just need to filter the results from above total number of issues
```bash
git log --oneline --grep="Merge pull request" <previous release tag>..<target branch> | wc -l
```
In reality since often we'll do this prior to the release, you can
just use the current branch as the target branch, like so for the `devel` branch:
```bash
git log --oneline --grep="Merge pull request" v0.3.0..devel | wc -l
```

### Create a graph with the number of commits per day

I let Claude create a script for me to analyze the git log and create a graph
with the number of commits and PRs per week.

First get the git log and save it to a file:
```bash
git log --pretty=format:'"%h","%an","%ad","%s"' > commit_history.csv
```

Then run the script:
```bash
python3 scripts/commit_analysis.py commit_history.csv [YYYYMMDD of last release] [optionally [YYYYMMDD of current date]]
```



