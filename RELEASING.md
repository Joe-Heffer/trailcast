# Releasing

Releases are automated via [release-please](https://github.com/googleapis/release-please) and triggered on every push to `main`.

## How it works

1. `release-please` reads commit messages on `main` and maintains a **Release PR** that accumulates changelog entries and bumps the version in `pyproject.toml`.
2. When the Release PR is merged, `release-please` creates a GitHub Release and tag (e.g. `v0.2.0`).
3. (Future) A publish step can be added to `.github/workflows/release.yml` to push to PyPI on tag creation.

## Conventional Commits

Commit messages **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) spec. `release-please` uses them to determine the next version and build the changelog.

### Format

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

### Types and their effect on versioning

| Type | Description | Version bump |
|------|-------------|--------------|
| `feat` | New user-facing feature | minor (`0.x.0`) |
| `fix` | Bug fix | patch (`0.0.x`) |
| `feat!` or `fix!` or any `BREAKING CHANGE:` footer | Breaking API change | major (`x.0.0`) |
| `chore` | Build/tooling/maintenance | none |
| `ci` | CI/CD changes | none |
| `docs` | Documentation only | none |
| `refactor` | Code restructuring without behaviour change | none |
| `test` | Test changes | none |
| `perf` | Performance improvement | patch |

### Examples

```
feat(forecast): add soil saturation index to rideability score
fix(weather): handle missing precipitation field from Open-Meteo
feat!: rename TrailInput.polyline to TrailInput.geometry
chore(deps): bump httpx to 0.28
docs: document CDS_API_KEY setup in CONTRIBUTING
```

### Breaking changes

Add a `BREAKING CHANGE:` footer (or append `!` to the type) to trigger a major bump:

```
feat!: rename TrailInput.polyline to TrailInput.geometry

BREAKING CHANGE: The `polyline` field on TrailInput has been renamed to
`geometry` to better reflect the accepted input types.
```

## Scopes

Scopes are optional but encouraged. Use the module/subsystem being changed:

- `forecast`, `weather`, `soil`, `terrain`, `cache`, `cli`, `models`, `deps`, `ci`

## Workflow file

The release workflow lives at [`.github/workflows/release.yml`](.github/workflows/release.yml) and runs on every push to `main`. It uses `googleapis/release-please-action@v5` with `release-type: python`, which knows how to update the `version` field in `pyproject.toml`.

## Making a release (step by step)

1. Merge one or more conventional-commit PRs into `main`.
2. `release-please` opens (or updates) a Release PR titled e.g. `chore(main): release 0.2.0`.
3. Review the auto-generated `CHANGELOG.md` entries in the Release PR.
4. Merge the Release PR — this creates the GitHub Release and tag automatically.
5. Verify the release appears at `https://github.com/Joe-Heffer/trailcast/releases`.

## Version policy

This project follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`). While the project is pre-1.0, breaking changes increment the minor version rather than the major version, matching `release-please`'s default behaviour for pre-release Python packages.
