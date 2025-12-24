# Pull Request Template

## Description

<!-- Provide a brief description of the changes in this PR -->

### What does this PR do?

<!-- Explain the purpose of this PR -->

### Why is this change necessary?

<!-- Explain the motivation or context for this change -->

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test updates
- [ ] CI/CD changes
- [ ] Dependency updates

## Related Issues

<!-- Link to related issues using GitHub keywords -->
<!-- Examples: Closes #123, Fixes #456, Relates to #789 -->

Closes #
Fixes #
Relates to #

## Changes Made

<!-- Provide a detailed list of changes -->

### Backend Changes
-
-

### Frontend Changes
-
-

### Infrastructure/Configuration Changes
-
-

### Documentation Changes
-
-

## How Has This Been Tested?

<!-- Describe the tests you ran and how to reproduce -->

### Test Configuration
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Manual testing

### Test Details
<!-- Describe what you tested -->

**Test Environment:**
- OS:
- Python version:
- Node version:

**Steps to test:**
1.
2.
3.

## Screenshots (if applicable)

<!-- Add screenshots or GIFs to demonstrate UI changes -->

### Before
<!-- Screenshot of before state -->

### After
<!-- Screenshot of after state -->

## Checklist

<!-- Mark completed items with an "x" -->

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings or errors

### Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have tested all affected features manually

### Documentation
- [ ] I have updated the README if needed
- [ ] I have updated API documentation if endpoints changed
- [ ] I have updated inline code comments
- [ ] I have updated the CHANGELOG (if applicable)

### Dependencies
- [ ] I have not introduced new dependencies
- [ ] OR: I have documented why new dependencies are necessary
- [ ] I have checked that all dependencies are secure and up-to-date

### Security
- [ ] My changes do not introduce security vulnerabilities
- [ ] I have not committed sensitive information (API keys, passwords, etc.)
- [ ] I have validated all user inputs
- [ ] I have handled errors appropriately

### Performance
- [ ] My changes do not negatively impact performance
- [ ] OR: I have documented performance trade-offs
- [ ] I have optimized database queries (if applicable)
- [ ] I have optimized API calls (if applicable)

### Clean Architecture
- [ ] My changes follow Clean Architecture principles
- [ ] Domain layer has no external dependencies
- [ ] Dependencies point inward (Frameworks → Adapters → Application → Domain)
- [ ] I have used dependency injection appropriately

### Breaking Changes
- [ ] This PR does not introduce breaking changes
- [ ] OR: I have documented breaking changes in the description
- [ ] OR: I have provided migration guide for breaking changes

## Deployment Notes

<!-- Any special deployment considerations -->

### Database Changes
- [ ] No database changes
- [ ] Schema changes (requires migration)
- [ ] Data migrations required

### Environment Variables
- [ ] No new environment variables
- [ ] New environment variables added (documented in .env.example)

### Configuration Changes
- [ ] No configuration changes
- [ ] Configuration files updated (documented below)

### Special Deployment Steps
<!-- List any special steps needed for deployment -->
1.
2.

## Rollback Plan

<!-- How to rollback if this change causes issues -->

**If this PR causes issues:**
1.
2.

## Additional Context

<!-- Add any other context about the PR here -->

### Known Limitations
<!-- List any known limitations of this implementation -->
-
-

### Future Improvements
<!-- Suggest potential future improvements -->
-
-

### Notes for Reviewers
<!-- Any specific areas you'd like reviewers to focus on -->
-
-

## Review Checklist (for Reviewers)

<!-- Reviewers should check these items -->

- [ ] Code follows project conventions and best practices
- [ ] Changes are well-tested and tests pass
- [ ] Documentation is clear and complete
- [ ] No security vulnerabilities introduced
- [ ] No performance regressions
- [ ] Breaking changes are documented
- [ ] Clean Architecture principles are followed
- [ ] Commit messages follow Conventional Commits format

---

<!--
Thank you for your contribution!
Please ensure all checklist items are complete before requesting review.
-->
