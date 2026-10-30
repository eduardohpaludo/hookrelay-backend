# ADR 001: Python version policy

- Status: Accepted
- Date: 2026-10-29

## Context

The project runs Python in three places, and until now they did not agree:

- Local development used Python 3.15.
- CI (GitHub Actions) ran Python 3.14.
- `pyproject.toml` declared no supported version, and the first CI draft passed `--target-version=py39` to ruff on the command line, a third, unrelated value.

Three different versions mean a green local run proves little about CI, and later about the runtime.

## Decision

Use **Python 3.14** as the single supported version for local development, CI and, for now, `requires-python`:

- `requires-python = ">=3.14"` in `pyproject.toml`.
- `python-version: "3.14"` in `.github/workflows/ci.yml`.

The rule behind the number: **development, CI and runtime use the same minor version.** The number itself is revisited whenever the runtime target changes.

## Alternatives considered

1. **Newest release (3.15, what my machine had).** Matches local today, but a brand-new minor version has the least library and platform support, and the managed runtime we will deploy to may not offer it yet. Rejected for now.
2. **Conservative older version (for example 3.11 or 3.12).** Maximum compatibility with managed runtimes, but it gives up newer language features for no current need, and the project has no consumer that requires it.
3. **Leave versions unpinned.** What we had. Rejected because it caused the mismatch this ADR resolves.

## Consequences

- Positive: a passing local run is strong evidence for CI. One version to reason about, upgrade and document.
- Negative: I have to recreate the local virtual environment, and I will not exercise 3.15 features or deprecations until we move.
- Upgrades become a deliberate change: bump all three places in one pull request and let CI confirm.