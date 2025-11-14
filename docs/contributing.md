title: Contributing
layout: default
---


# Contributing to VisionX


Thank you for contributing. This file describes a minimal, consistent workflow to keep the repository healthy.


## Code of Conduct


Be respectful and constructive.


## Development workflow


1. Keep `main` protected. Use branches for work:
- `feature/<short-description>` for new features
- `fix/<short-description>` for bug fixes
- `chore/<short-description>` for maintenance


2. Open issues for any bug, enhancement, or task.


3. Create a pull request that references the issue (when applicable) and describes the change.


## Commit message style


Use terse, imperative messages. Example:
> Add Vosk offline recognizer Fix audio clip truncation when buffer fills

## Tests and checks


- Add unit tests where applicable.
- Keep changes small and reviewable.


## Local development tips


- Use `venv` for dependency isolation.
- Use `flake8` / `black` if you want consistent style.


## Issues template (suggestion)


Title: `Short summary`


Body:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, venv)


## Pull request checklist


- [ ] Linked to an issue (if applicable)
- [ ] Tests added / updated
- [ ] Documentation updated
- [ ] Self-review passed
