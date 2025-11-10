# Workflow

## Branching Model
- **main** → stable version only.
- **dev** → main development branch.
- **feature/** → for new features.
- **fix/** → for bug fixes.

## Contribution Process
1. Clone the repository.
2. Create a new branch (e.g., `feature/audio-module`).
3. Commit your changes.
4. Push the branch.
5. Create a Pull Request (PR) and wait for review.

## Code Review
- Every PR must be reviewed by at least one team member.
- Use comments for suggestions or improvements.

## Environment Setup
```bash
git clone git@github.com:VissionX/VisionX.git
cd VisionX
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

