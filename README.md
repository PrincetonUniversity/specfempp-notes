# Specfempp-Notes

This repo is just for keeping track of notes, slides, etc., that are relevant for the development of [SPECFEM++](https://github.com/PrincetonUniversity/SPECFEMPP).


## LLNL-Princeton PE & EM Hackathon link

**Poro-Elastic (PE)**

- [Project](https://github.com/orgs/PrincetonUniversity/projects/47)
- [Issues](https://github.com/PrincetonUniversity/SPECFEMPP/issues?q=is%3Aissue%20state%3Aopen%20project%3APrincetonUniversity%2F47)
- [Pull Requests](https://github.com/PrincetonUniversity/SPECFEMPP/pulls?q=is%3Apr+is%3Aopen+project%3Aproject%3APrincetonUniversity%2F47)

**Electro-magnetic (EM)**

- [Project](https://github.com/orgs/PrincetonUniversity/projects/48)
- [Issues](https://github.com/PrincetonUniversity/SPECFEMPP/issues?q=is%3Aissue%20state%3Aopen%20project%3APrincetonUniversity%2F48)
- [Pull Requests](https://github.com/PrincetonUniversity/SPECFEMPP/pulls?q=is%3Apr+is%3Aopen+project%3APrincetonUniversity%2F48)


--

Project workflow (for any GitHub project) assuming that you have “forked” the repo:

1. Sync your fork 
    1. On your GitHub SPECFEM fork, choose a base branch (e.g. PE)
    2. Click “Sync fork”
2. Get or update the branch in your local terminal
    1. Get
        1. `git clone git@github.com:<username>/SPECFEMPP.git`
        2. `git checkout <base-branch>`
    2. Update
        1. `git checkout <base-branch>`
        2. `git pull origin <base-branch>`
3. Choose Issue to work on in the Project, e.g. #612 (Update the timescheme)
    1. Make sure to assign yourself to the issue!
5. Create branch to work on
    1. `git checkout -b issue-<issue number> # e.g. issue-602`
6. Make and commit changes
    1. Make changes to files
    2. Stage changes: `git add <file you have worked on>`
    3. Commit changes: `git commit -m ‘Commit message (what you did)’`
    4. Upload changes: `git push origin issue-<issue number>`
7. On Github make a pull request (PR) from your new branch to the base-branch in PrincetonUniversity/SPECFEMPP
    1. Click on the PR tab on your GitHub fork page
    2. Choose to compare across forks
    3. Choose destination to PrincetonUniversity/SPECFEMPP at base branch 
    4. Choose source to be username/issue-#issuenumber
    5. Now, click “Create Pull request"
    6. You will be prompted to fill out the description about the PR
8. The PR will now be reviewed by others and will eventually be merged, or you will be asked for some updates.
9. While you wait for approval you can restart at 1.
