# Git Beginner Guide

This guide is for first-time contributors.

## 1. Fork the Repo
1. Open the project repo in GitHub.
2. Click `Fork`.
3. Keep it under your own account.

## 2. Clone Your Fork
```bash
git clone https://github.com/<your-username>/cu-routing.git
cd cu-routing
```

## 3. Add Original Repo as Upstream
```bash
git remote add upstream https://github.com/Temiloluwa-Ogundiran/cu-routing.git
git remote -v
```

## 4. Create a Branch
```bash
git checkout -b feature/issue-<number>-short-name
```

## 5. Make Your Changes
- Edit only files needed for your issue.
- Run tests:
```bash
pytest -q
```

## 6. Commit
```bash
git add .
git commit -m "feat: short clear message"
```

## 7. Push
```bash
git push origin feature/issue-<number>-short-name
```

## 8. Open Pull Request
1. Go to your fork on GitHub.
2. Click `Compare & pull request`.
3. Use base repo: `Temiloluwa-Ogundiran/cu-routing`.
4. Fill the PR template.
5. Link the issue (`Closes #<number>`).

## 9. Update Branch if Main Changes
```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
git checkout feature/issue-<number>-short-name
git merge main
```

## Common Mistakes to Avoid
- Working directly on `main`.
- One PR for many unrelated issues.
- Not linking issue in PR.
- Forgetting to run tests before pushing.
