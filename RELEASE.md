
Release command for V0.1.0
```bash
git add pyproject.toml
git commit -m "Fix invalid PyPI classifier"
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0
git tag v0.1.0
git push origin v0.1.0
```



Release command for V0.1.1
```bash
git add .
git commit -m "Fix Version number"
git push origin :refs/tags/v0.1.1
git tag -d v0.1.0
git tag v0.1.1
git push origin v0.1.1
```