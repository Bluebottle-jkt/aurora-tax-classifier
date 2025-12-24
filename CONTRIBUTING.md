# Contributing to AURORA Tax Classifier

Thank you for your interest in contributing to the AURORA Tax Classifier project! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Branch Naming Conventions](#branch-naming-conventions)
5. [Commit Message Guidelines](#commit-message-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Code Style Guidelines](#code-style-guidelines)
8. [Testing Requirements](#testing-requirements)
9. [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of professional conduct. By participating, you are expected to:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Acknowledge and respect differing viewpoints
- Prioritize the best outcome for the project and community

## Getting Started

### Prerequisites

Before you begin contributing, ensure you have:

1. Git installed and configured
2. Python 3.9+ for backend development
3. Node.js 18+ and npm for frontend development
4. Docker and Docker Compose (optional, for containerized development)
5. A code editor (VSCode recommended)

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/aurora-tax-classifier.git
   cd aurora-tax-classifier
   ```

3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/aurora-tax-classifier.git
   ```

4. **Set up the backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Set up the frontend**:
   ```bash
   cd frontend
   npm install
   ```

6. **Copy environment configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

## Development Workflow

### 1. Sync with Upstream

Before starting new work, always sync with the upstream repository:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### 2. Create a Feature Branch

Create a new branch for your work (see [Branch Naming Conventions](#branch-naming-conventions)):

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Write clean, maintainable code
- Follow the project's code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 4. Commit Your Changes

Follow our [Commit Message Guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat: add new tax classification feature"
```

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

Open a pull request from your fork to the upstream repository.

## Branch Naming Conventions

Use the following prefixes for branch names:

### Branch Types

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features or enhancements | `feature/add-bulk-upload` |
| `fix/` | Bug fixes | `fix/correct-classification-logic` |
| `hotfix/` | Critical production fixes | `hotfix/security-vulnerability` |
| `refactor/` | Code refactoring | `refactor/simplify-prediction-service` |
| `docs/` | Documentation updates | `docs/update-api-reference` |
| `test/` | Adding or updating tests | `test/add-unit-tests-for-service` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |
| `perf/` | Performance improvements | `perf/optimize-database-queries` |
| `style/` | Code style changes (formatting, etc.) | `style/apply-black-formatting` |
| `ci/` | CI/CD pipeline changes | `ci/add-github-actions-workflow` |

### Branch Naming Rules

1. Use lowercase letters
2. Use hyphens to separate words
3. Be descriptive but concise
4. Include issue number if applicable: `feature/123-add-export-feature`

### Examples

```bash
# Good branch names
feature/add-risk-scoring
fix/upload-validation-error
docs/update-installation-guide
refactor/domain-layer-structure

# Bad branch names
feature/new-stuff
fix-bug
my-branch
UPDATE_DOCS
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for clear and structured commit messages.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, missing semicolons, etc.) |
| `refactor` | Code refactoring without changing functionality |
| `perf` | Performance improvements |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks, dependency updates |
| `ci` | CI/CD pipeline changes |
| `build` | Build system or external dependency changes |
| `revert` | Reverting a previous commit |

### Scope (Optional)

The scope specifies the area of the codebase affected:

- `api` - API endpoints
- `ui` - User interface
- `ml` - Machine learning models
- `db` - Database
- `domain` - Domain layer
- `infra` - Infrastructure
- `config` - Configuration

### Subject

- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize the first letter
- No period at the end
- Limit to 50 characters

### Body (Optional)

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Separate from subject with a blank line

### Footer (Optional)

- Reference issues: `Closes #123`, `Fixes #456`
- Note breaking changes: `BREAKING CHANGE: description`

### Examples

#### Simple commit:
```
feat(api): add batch prediction endpoint
```

#### Commit with body:
```
fix(ml): correct probability calculation in risk scoring

The previous implementation was using incorrect weights for
fiscal correction predictions, leading to inflated risk scores.
This fix adjusts the calculation to match the specification.

Closes #234
```

#### Breaking change:
```
feat(api): redesign authentication flow

BREAKING CHANGE: API now requires JWT tokens instead of API keys.
Update your client applications to use the new auth endpoint.

Closes #456
```

#### Multiple changes:
```
chore: update project dependencies

- Upgrade FastAPI to 0.109.0
- Update React to 18.2.0
- Bump security dependencies

Closes #567
```

## Pull Request Process

### Before Submitting

1. **Ensure your code builds and runs**:
   ```bash
   # Backend
   cd backend
   python -m pytest tests/

   # Frontend
   cd frontend
   npm run build
   npm run test
   ```

2. **Check code quality**:
   ```bash
   # Backend - Run linting and formatting
   cd backend
   black src/
   flake8 src/
   mypy src/

   # Frontend - Run linting
   cd frontend
   npm run lint
   ```

3. **Update documentation** if you've changed:
   - API endpoints
   - Configuration options
   - User-facing features
   - Development setup

4. **Write or update tests** for:
   - New features
   - Bug fixes
   - Changed behavior

### Creating the Pull Request

1. **Use a clear, descriptive title**:
   - Good: `feat(api): add CSV export for prediction results`
   - Bad: `Update files` or `Fix bug`

2. **Fill out the PR template** completely:
   ```markdown
   ## Description
   Brief description of what this PR does

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex logic
   - [ ] Documentation updated
   - [ ] No new warnings generated
   - [ ] Tests pass locally
   ```

3. **Link related issues**:
   - Use keywords: `Closes #123`, `Fixes #456`, `Relates to #789`

4. **Request reviewers**:
   - Tag relevant maintainers or team members

### During Review

1. **Respond to feedback promptly**
2. **Make requested changes** in new commits (don't force-push during review)
3. **Discuss disagreements** constructively
4. **Mark conversations as resolved** after addressing them

### After Approval

1. **Squash commits** if requested (combine related commits)
2. **Rebase on main** if needed:
   ```bash
   git fetch upstream
   git rebase upstream/main
   git push origin feature/your-feature --force-with-lease
   ```

3. **Wait for final approval** before merging
4. **Delete your branch** after the PR is merged

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 88)
- Use type hints for function signatures
- Write docstrings for classes and functions (Google style)

Example:
```python
from typing import List, Optional
from domain.entities import PredictionRow

def calculate_risk_score(
    predictions: List[PredictionRow],
    threshold: float = 0.7
) -> float:
    """
    Calculate aggregate risk score from predictions.

    Args:
        predictions: List of prediction rows to analyze
        threshold: Confidence threshold for high-risk classification

    Returns:
        Calculated risk score between 0.0 and 1.0

    Raises:
        ValueError: If predictions list is empty
    """
    if not predictions:
        raise ValueError("Predictions list cannot be empty")

    # Implementation here
    pass
```

### TypeScript/JavaScript (Frontend)

- Follow the project's ESLint configuration
- Use TypeScript for type safety
- Prefer functional components and hooks
- Use meaningful variable and function names

Example:
```typescript
interface PredictionResult {
  id: string;
  taxObject: string;
  confidence: number;
  riskScore: number;
}

const PredictionList: React.FC<{ predictions: PredictionResult[] }> = ({
  predictions
}) => {
  return (
    <div className="prediction-list">
      {predictions.map((prediction) => (
        <PredictionCard key={prediction.id} prediction={prediction} />
      ))}
    </div>
  );
};
```

### General Guidelines

- Keep functions small and focused (single responsibility)
- Avoid deep nesting (max 3-4 levels)
- Use meaningful names for variables, functions, and classes
- Comment complex logic, not obvious code
- Prefer composition over inheritance
- Write self-documenting code when possible

## Testing Requirements

### Backend Testing

All backend code should include:

1. **Unit tests** for individual functions and classes
2. **Integration tests** for use cases and services
3. **API tests** for endpoints

Minimum coverage: **80%**

Example:
```python
import pytest
from application.use_cases import CreateJobUseCase

def test_create_job_use_case_success():
    """Test successful job creation."""
    # Arrange
    use_case = CreateJobUseCase(mock_repository)

    # Act
    result = use_case.execute(valid_input)

    # Assert
    assert result.is_success
    assert result.job_id is not None
```

### Frontend Testing

Frontend code should include:

1. **Component tests** using React Testing Library
2. **Hook tests** for custom hooks
3. **Integration tests** for complex workflows

Example:
```typescript
import { render, screen } from '@testing-library/react';
import { PredictionCard } from './PredictionCard';

describe('PredictionCard', () => {
  it('displays prediction details correctly', () => {
    const prediction = {
      id: '1',
      taxObject: 'Harta',
      confidence: 0.95,
      riskScore: 0.2
    };

    render(<PredictionCard prediction={prediction} />);

    expect(screen.getByText('Harta')).toBeInTheDocument();
    expect(screen.getByText('95%')).toBeInTheDocument();
  });
});
```

### Running Tests

```bash
# Backend - Run all tests
cd backend
pytest

# Backend - Run with coverage
pytest --cov=src tests/

# Frontend - Run all tests
cd frontend
npm test

# Frontend - Run with coverage
npm test -- --coverage
```

## Documentation

### What to Document

1. **Code**:
   - Public APIs and interfaces
   - Complex algorithms or business logic
   - Non-obvious design decisions

2. **Features**:
   - User-facing features in README or user guide
   - API endpoints in API documentation
   - Configuration options

3. **Setup and Deployment**:
   - Installation instructions
   - Environment configuration
   - Deployment procedures

### Documentation Style

- Use clear, concise language
- Include code examples
- Add diagrams for complex flows
- Keep documentation up-to-date with code changes

## Questions or Need Help?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Reach out to maintainers for guidance

## License

By contributing to AURORA Tax Classifier, you agree that your contributions will be licensed under the project's license.

---

Thank you for contributing to AURORA Tax Classifier! Your efforts help make this project better for everyone.
