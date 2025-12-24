# GitHub Setup Guide for AURORA Tax Classifier

This guide will walk you through setting up your local Git repository and connecting it to GitHub.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initialize Git Repository](#initialize-git-repository)
3. [Create Initial Commit](#create-initial-commit)
4. [Create GitHub Repository](#create-github-repository)
5. [Connect Local Repository to GitHub](#connect-local-repository-to-github)
6. [Push to GitHub](#push-to-github)
7. [Verify Setup](#verify-setup)
8. [Next Steps](#next-steps)
9. [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:

- [x] Git installed on your system
- [x] GitHub account created
- [x] Git configured with your name and email:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```
- [x] GitHub authentication set up (SSH keys or Personal Access Token)

### Setting Up GitHub Authentication

#### Option 1: SSH Keys (Recommended)

1. **Generate SSH key** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. **Add SSH key to ssh-agent**:
   ```bash
   # Start the ssh-agent
   eval "$(ssh-agent -s)"

   # Add your SSH private key
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Add SSH key to GitHub**:
   - Copy your public key:
     ```bash
     cat ~/.ssh/id_ed25519.pub
     ```
   - Go to GitHub Settings > SSH and GPG keys > New SSH key
   - Paste your public key and save

4. **Test connection**:
   ```bash
   ssh -T git@github.com
   ```

#### Option 2: Personal Access Token (PAT)

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (if using GitHub Actions)
4. Generate and save the token securely (you won't see it again!)
5. Use this token as your password when prompted by Git

For more details, see: https://docs.github.com/en/authentication

## Initialize Git Repository

### Step 1: Navigate to Project Directory

Open your terminal and navigate to the project:

```bash
cd d:\TaxObjectFinder\aurora-tax-classifier
```

### Step 2: Initialize Git

Run the initialization script we created:

```bash
# Windows
.\init_git.bat

# Or run git directly
git init
```

You should see:
```
Initialized empty Git repository in d:/TaxObjectFinder/aurora-tax-classifier/.git/
```

### Step 3: Verify Git Initialization

Check the Git status:

```bash
git status
```

You should see a list of untracked files.

## Create Initial Commit

### Step 1: Review Files to Commit

Before staging files, review what will be committed:

```bash
git status
```

The `.gitignore` file is already configured to exclude:
- Virtual environments (`venv/`, `node_modules/`)
- Environment files (`.env` - only `.env.example` will be tracked)
- Build artifacts
- IDE settings
- Temporary files

### Step 2: Stage All Files

Stage all files for the initial commit:

```bash
git add .
```

### Step 3: Verify Staged Files

Check what will be committed:

```bash
git status
```

Review the list and ensure no sensitive files are included (like `.env` with actual credentials).

### Step 4: Create Initial Commit

Commit the files with a meaningful message:

```bash
git commit -m "Initial commit: AURORA Tax Classifier project structure

- Set up clean architecture with Domain-Driven Design
- Configure backend API with FastAPI
- Set up frontend with React and TypeScript
- Add Docker support for containerized deployment
- Include comprehensive documentation
- Configure development environment with example configs"
```

### Step 5: Verify Commit

Check the commit log:

```bash
git log
```

You should see your initial commit.

## Create GitHub Repository

### Option 1: Using GitHub Web Interface

1. **Go to GitHub**: https://github.com/new

2. **Configure repository**:
   - Repository name: `aurora-tax-classifier`
   - Description: `AURORA - Indonesian Tax Classification System using ML for PPh Object and Fiscal Correction Prediction`
   - Visibility: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

3. **Click "Create repository"**

### Option 2: Using GitHub CLI (if installed)

```bash
gh repo create aurora-tax-classifier --public --description "AURORA - Indonesian Tax Classification System" --source=. --remote=origin
```

## Connect Local Repository to GitHub

After creating the GitHub repository, you'll see setup instructions. Follow these steps:

### Step 1: Add Remote Origin

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# If using HTTPS
git remote add origin https://github.com/YOUR_USERNAME/aurora-tax-classifier.git

# If using SSH (recommended)
git remote add origin git@github.com:YOUR_USERNAME/aurora-tax-classifier.git
```

### Step 2: Verify Remote

Check that the remote was added correctly:

```bash
git remote -v
```

You should see:
```
origin  git@github.com:YOUR_USERNAME/aurora-tax-classifier.git (fetch)
origin  git@github.com:YOUR_USERNAME/aurora-tax-classifier.git (push)
```

### Step 3: Set Default Branch Name

Ensure you're using `main` as the default branch:

```bash
git branch -M main
```

## Push to GitHub

### Step 1: Push Initial Commit

Push your code to GitHub:

```bash
git push -u origin main
```

The `-u` flag sets the upstream tracking, so future pushes can simply use `git push`.

### Step 2: Enter Credentials (if prompted)

- **SSH**: No credentials needed (uses SSH key)
- **HTTPS**: Enter your GitHub username and Personal Access Token

### Step 3: Wait for Upload

The initial push may take a few minutes depending on:
- Project size
- Your internet connection
- Number of files

You'll see output like:
```
Enumerating objects: 150, done.
Counting objects: 100% (150/150), done.
Delta compression using up to 8 threads
Compressing objects: 100% (120/120), done.
Writing objects: 100% (150/150), 1.5 MiB | 500 KiB/s, done.
Total 150 (delta 25), reused 0 (delta 0)
To github.com:YOUR_USERNAME/aurora-tax-classifier.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## Verify Setup

### Step 1: Check GitHub Repository

1. Go to your repository on GitHub: `https://github.com/YOUR_USERNAME/aurora-tax-classifier`
2. Verify that all files are visible
3. Check that the README.md is displayed on the main page

### Step 2: Verify Local Configuration

Check your local Git configuration:

```bash
# Check remote
git remote -v

# Check current branch
git branch

# Check tracking
git branch -vv
```

### Step 3: Test Push and Pull

Make a small change to test the connection:

```bash
# Make a small change
echo "# Last updated: $(date)" >> README.md

# Commit the change
git add README.md
git commit -m "docs: update README with last updated timestamp"

# Push to GitHub
git push

# Verify it appears on GitHub
```

## Next Steps

### 1. Set Up Branch Protection

Protect your `main` branch to enforce best practices:

1. Go to repository Settings > Branches
2. Add branch protection rule for `main`:
   - Require pull request reviews before merging
   - Require status checks to pass
   - Require branches to be up to date before merging
   - Include administrators (optional)

### 2. Configure GitHub Actions (Optional)

Set up CI/CD workflows:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Run tests
        run: |
          pip install -r backend/requirements.txt
          pytest backend/tests/
```

### 3. Add Repository Topics

Add topics to make your repository discoverable:
- Go to repository main page
- Click the gear icon next to "About"
- Add topics: `machine-learning`, `tax-classification`, `fastapi`, `react`, `indonesia`, `ddd`, `clean-architecture`

### 4. Create Issue Templates

Add issue templates for bugs and features:

```bash
mkdir -p .github/ISSUE_TEMPLATE
```

Create `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`.

### 5. Add a License

If you haven't already, add a LICENSE file:

1. Go to repository main page
2. Click "Add file" > "Create new file"
3. Name it `LICENSE`
4. Click "Choose a license template"
5. Select appropriate license (MIT, Apache 2.0, etc.)

### 6. Set Up Collaborators

If working with a team:
1. Go to Settings > Collaborators
2. Add team members with appropriate permissions

### 7. Enable GitHub Features

Consider enabling:
- **Issues**: For bug tracking and feature requests
- **Projects**: For project management
- **Discussions**: For community Q&A
- **Wiki**: For additional documentation
- **Sponsorships**: If accepting donations

## Troubleshooting

### Problem: "Permission denied (publickey)"

**Solution**: Your SSH key is not configured correctly.

```bash
# Verify SSH key exists
ls -la ~/.ssh

# Generate new key if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub (copy and paste)
cat ~/.ssh/id_ed25519.pub
```

### Problem: "Authentication failed" with HTTPS

**Solution**: Use a Personal Access Token instead of your password.

1. Generate a PAT (see Prerequisites section)
2. Use the token as your password when prompted

### Problem: "Repository not found"

**Solution**: Check the remote URL.

```bash
# View current remote
git remote -v

# Update remote URL
git remote set-url origin git@github.com:YOUR_USERNAME/aurora-tax-classifier.git
```

### Problem: Large files causing push to fail

**Solution**: Use Git LFS for large files.

```bash
# Install Git LFS
git lfs install

# Track large file types
git lfs track "*.joblib"
git lfs track "*.csv"

# Commit .gitattributes
git add .gitattributes
git commit -m "chore: configure Git LFS for large files"
git push
```

### Problem: `.env` file was committed by accident

**Solution**: Remove it from Git history.

```bash
# Remove from current commit
git rm --cached .env

# Commit the removal
git commit -m "chore: remove .env from version control"

# Ensure .gitignore includes .env
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: update .gitignore to exclude .env"

# Push changes
git push
```

**Important**: If the file was already pushed, consider rotating any secrets it contained.

### Problem: Merge conflicts

**Solution**: Resolve conflicts manually.

```bash
# Pull latest changes
git pull origin main

# If conflicts occur, open the conflicted files and resolve
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# After resolving, mark as resolved
git add <resolved-file>

# Complete the merge
git commit -m "merge: resolve conflicts with origin/main"
git push
```

### Problem: Need to undo last commit

**Solution**: Use git reset or git revert.

```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Undo last commit and discard changes (DANGER!)
git reset --hard HEAD~1

# Create a new commit that reverses the last commit (safer)
git revert HEAD
```

## Useful Git Commands Reference

### Daily Workflow

```bash
# Check status
git status

# Stage changes
git add <file>
git add .

# Commit changes
git commit -m "type: description"

# Push to remote
git push

# Pull from remote
git pull

# View history
git log --oneline --graph
```

### Branch Management

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# List branches
git branch -a

# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

### Syncing

```bash
# Fetch changes without merging
git fetch origin

# Pull and rebase
git pull --rebase origin main

# Push force (use with caution!)
git push --force-with-lease
```

### Inspection

```bash
# Show changes
git diff

# Show staged changes
git diff --staged

# Show file history
git log --follow <file>

# Show who changed what
git blame <file>
```

## Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitHub Skills](https://skills.github.com/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Getting Help

If you encounter issues not covered in this guide:

1. Check the [GitHub Documentation](https://docs.github.com/)
2. Search for your error message online
3. Ask for help in the project discussions
4. Open an issue describing your problem

---

**Last Updated**: 2025-12-24

Welcome to collaborative development with Git and GitHub!
