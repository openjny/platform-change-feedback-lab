# Agent guide

- Read [README.md](README.md) for what the planner models and how to verify changes.
- Keep synthetic profiles in `profiles/`, planner behavior tests in `tests/`,
  and feedback policy separate from the planner.
- Keep the planner offline and dependency-free. Do not query or deploy cloud
  infrastructure. Do not inspect credentials, other repositories, or session
  directories.
- Follow [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a change.
