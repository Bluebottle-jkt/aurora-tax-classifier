# Git Quick Reference for AURORA Tax Classifier

Quick reference guide for common Git operations in the AURORA Tax Classifier project.

## Table of Contents

- [Setup Commands](#setup-commands)
- [Daily Workflow](#daily-workflow)
- [Branch Operations](#branch-operations)
- [Committing Changes](#committing-changes)
- [Syncing with Remote](#syncing-with-remote)
- [Viewing History](#viewing-history)
- [Undoing Changes](#undoing-changes)
- [Troubleshooting](#troubleshooting)

## Setup Commands

### First-Time Setup

```bash
# Configure Git (run once per machine)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository (already done via init_git.bat)
git init

# Add remote repository
git remote add origin git@github.com:YOUR_USERNAME/aurora-tax-classifier.git

# Verify remote
git remote -v

# Set main branch
git branch -M main

# First push
git push -u origin main
```

## Daily Workflow

### Starting Your Day

```bash
# Update your local repository
git checkout main
git pull origin main

# Check current status
git status

# See what you're working on
git branch
```

### Working on a Feature

```bash
# Create a new feature branch
git checkout -b feature/your-feature-name

# Make changes to files...

# Check what changed
git status
git diff

# Stage specific files
git add path/to/file

# Or stage all changes
git add .

# Commit with a message
git commit -m "feat: add your feature description"

# Push to remote
git push -u origin feature/your-feature-name
```

### Ending Your Day

```bash
# Ensure all changes are committed
git status

# Push any local commits
git push

# Switch back to main if needed
git checkout main
```

## Branch Operations

### Creating Branches

```bash
# Create and switch to a new branch
git checkout -b feature/new-feature

# Create branch without switching
git branch feature/new-feature

# Create branch from specific commit
git checkout -b hotfix/bug-fix abc123
```

### Switching Branches

```bash
# Switch to existing branch
git checkout main
git checkout feature/my-feature

# Switch to previous branch
git checkout -
```

### Listing Branches

```bash
# List local branches
git branch

# List all branches (including remote)
git branch -a

# List branches with last commit
git branch -v
```

### Deleting Branches

```bash
# Delete local branch (safe - won't delete if unmerged)
git branch -d feature/old-feature

# Force delete local branch
git branch -D feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

### Merging Branches

```bash
# Merge feature branch into main
git checkout main
git merge feature/my-feature

# Merge with no fast-forward (creates merge commit)
git merge --no-ff feature/my-feature
```

## Committing Changes

### Staging Files

```bash
# Stage specific file
git add backend/src/api/routes.py

# Stage multiple files
git add file1.py file2.py

# Stage all Python files in directory
git add backend/src/**/*.py

# Stage all changes
git add .

# Stage all, including deletions
git add -A

# Stage interactively
git add -p
```

### Committing

```bash
# Commit with message
git commit -m "fix: correct validation logic"

# Commit with detailed message
git commit -m "feat: add batch processing" -m "- Implement queue system" -m "- Add progress tracking" -m "- Update documentation"

# Commit all tracked changes (skip staging)
git commit -am "docs: update README"

# Amend last commit (change message or add files)
git commit --amend -m "fix: correct validation logic (updated)"

# Amend without changing message
git commit --amend --no-edit
```

### Commit Message Examples

Follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
# Features
git commit -m "feat(api): add CSV export endpoint"
git commit -m "feat(ui): implement dark mode toggle"

# Bug fixes
git commit -m "fix(ml): correct probability calculation"
git commit -m "fix(api): handle empty file upload"

# Documentation
git commit -m "docs: update installation guide"
git commit -m "docs(api): add endpoint examples"

# Refactoring
git commit -m "refactor(domain): simplify entity structure"

# Tests
git commit -m "test(api): add integration tests for upload"

# Chores
git commit -m "chore: update dependencies"
git commit -m "chore(deps): bump fastapi to 0.109.0"

# Performance
git commit -m "perf(db): add index on job_id column"

# Breaking changes
git commit -m "feat(api)!: redesign authentication flow"
```

## Syncing with Remote

### Pushing Changes

```bash
# Push to current branch's upstream
git push

# Push and set upstream for first time
git push -u origin feature/my-feature

# Push all branches
git push --all

# Force push (use with caution!)
git push --force-with-lease

# Push tags
git push --tags
```

### Pulling Changes

```bash
# Pull from current branch's upstream
git pull

# Pull from specific branch
git pull origin main

# Pull with rebase instead of merge
git pull --rebase

# Fetch without merging
git fetch origin

# Fetch all remotes
git fetch --all
```

### Keeping Fork Updated

```bash
# Add upstream remote (once)
git remote add upstream git@github.com:ORIGINAL_OWNER/aurora-tax-classifier.git

# Fetch upstream changes
git fetch upstream

# Merge upstream main into your main
git checkout main
git merge upstream/main

# Or rebase on upstream main
git rebase upstream/main

# Push updates to your fork
git push origin main
```

## Viewing History

### Log Commands

```bash
# View commit history
git log

# One-line summary
git log --oneline

# Graph view
git log --oneline --graph --all

# Last N commits
git log -5

# Show stats
git log --stat

# Show patches
git log -p

# By author
git log --author="Your Name"

# By date
git log --since="2024-01-01"
git log --until="2024-12-31"

# By message
git log --grep="fix"

# File history
git log --follow path/to/file
```

### Diff Commands

```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged

# Show changes in specific file
git diff path/to/file

# Compare branches
git diff main feature/my-feature

# Compare with remote
git diff origin/main

# Show changes by specific commit
git show abc123

# Word diff (better for text)
git diff --word-diff
```

### Blame and History

```bash
# Show who changed each line
git blame path/to/file

# Ignore whitespace in blame
git blame -w path/to/file

# Show file at specific commit
git show abc123:path/to/file
```

## Undoing Changes

### Unstaging Files

```bash
# Unstage specific file
git restore --staged path/to/file

# Unstage all files
git restore --staged .

# Old syntax (still works)
git reset HEAD path/to/file
```

### Discarding Changes

```bash
# Discard changes in working directory
git restore path/to/file

# Discard all changes
git restore .

# Old syntax (still works)
git checkout -- path/to/file
```

### Undoing Commits

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes unstaged
git reset HEAD~1

# Undo last commit, discard changes (DANGEROUS!)
git reset --hard HEAD~1

# Undo multiple commits
git reset --soft HEAD~3

# Create new commit that reverses changes (safer)
git revert HEAD

# Revert specific commit
git revert abc123
```

### Cleaning Working Directory

```bash
# Show what would be removed
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd

# Remove ignored files too
git clean -fdx
```

## Troubleshooting

### Merge Conflicts

```bash
# See conflicted files
git status

# After resolving conflicts in files:
git add path/to/resolved-file

# Continue merge
git commit

# Abort merge
git merge --abort
```

### Stashing Changes

```bash
# Stash current changes
git stash

# Stash with message
git stash save "WIP: feature implementation"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply specific stash
git stash apply stash@{2}

# Apply and remove stash
git stash pop

# Remove specific stash
git stash drop stash@{2}

# Clear all stashes
git stash clear
```

### Finding Lost Commits

```bash
# Show all reference updates
git reflog

# Checkout lost commit
git checkout abc123

# Create branch from lost commit
git checkout -b recovery abc123
```

### Fixing Mistakes

```bash
# Forgot to add a file to last commit
git add forgotten-file.py
git commit --amend --no-edit

# Change last commit message
git commit --amend -m "New commit message"

# Pushed wrong code (create fix commit instead of rewriting history)
git revert HEAD
git push
```

## Common Workflows

### Feature Development Workflow

```bash
# 1. Start from updated main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/user-authentication

# 3. Work and commit regularly
git add .
git commit -m "feat(auth): implement login endpoint"

# 4. Keep branch updated
git fetch origin main
git merge origin/main

# 5. Push feature branch
git push -u origin feature/user-authentication

# 6. Create pull request on GitHub
# 7. After review and merge, clean up
git checkout main
git pull origin main
git branch -d feature/user-authentication
```

### Hotfix Workflow

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Fix the bug
git add .
git commit -m "fix: resolve critical security issue"

# 3. Push and create PR
git push -u origin hotfix/critical-bug

# 4. After merge, update local main
git checkout main
git pull origin main
git branch -d hotfix/critical-bug
```

### Release Workflow

```bash
# 1. Create release branch
git checkout -b release/v1.0.0

# 2. Update version numbers, changelog
git add .
git commit -m "chore: prepare v1.0.0 release"

# 3. Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"

# 4. Push branch and tag
git push origin release/v1.0.0
git push origin v1.0.0

# 5. Merge to main and develop
git checkout main
git merge release/v1.0.0
git push origin main
```

## Project-Specific Tips

### Before Committing

Always check these before committing:

```bash
# 1. Run tests
cd backend && pytest
cd frontend && npm test

# 2. Check code style
cd backend && black src/ && flake8 src/
cd frontend && npm run lint

# 3. Verify no secrets
git diff --staged | grep -i "password\|secret\|key"

# 4. Review changes
git status
git diff --staged
```

### Useful Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = restore --staged
    last = log -1 HEAD
    lg = log --oneline --graph --all
    undo = reset --soft HEAD~1
```

Usage:
```bash
git st          # Instead of git status
git co main     # Instead of git checkout main
git lg          # Pretty log
```

## Emergency Commands

### "Oh no, I committed to the wrong branch!"

```bash
# Reset branch to before the commit
git reset HEAD~ --soft

# Stash the changes
git stash

# Switch to correct branch
git checkout correct-branch

# Apply the stashed changes
git stash pop

# Commit again
git commit -m "feat: add feature (on correct branch)"
```

### "I accidentally committed a secret!"

```bash
# 1. Remove the file
git rm --cached .env

# 2. Ensure it's in .gitignore
echo ".env" >> .gitignore

# 3. Commit the removal
git add .gitignore
git commit -m "chore: remove secret file from tracking"

# 4. Force push (if already pushed)
git push --force-with-lease

# 5. IMPORTANT: Rotate the exposed secret!
```

### "I need to undo a public commit!"

```bash
# Use revert instead of reset (safer for public history)
git revert abc123
git push
```

## Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)

---

**Last Updated**: 2025-12-24

Keep this reference handy for quick Git operations!
