# pdm-autoexport

![Github Actions](https://github.com/frostming/pdm-autoexport/workflows/Tests/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/pdm-autoexport?logo=python&logoColor=%23cccccc)](https://pypi.org/project/pdm-autoexport)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)

A PDM plugin to sync the exported files with the project file.

## Installation

Install the plugin with PDM CLI:

```bash
pdm plugin add pdm-autoexport
```

Or using `pipx inject`:

```bash
pipx inject pdm pdm-autoexport
```

## Usage

Configure the requirement mapping in `pyproject.toml`:

```toml
[[tool.pdm.autoexport]]
filename = "requirements/prod.txt"
groups = ["default"]

[[tool.pdm.autoexport]]
filename = "setup.py"
format = "setuppy"
```

Then the requirement files will be synced every time when the lock file is updated.

## Configuration

The configuration is an array of table `[[tool.pdm.autoexport]]` where each item may contain the following keys:

- `filename` (required): The path to the exported file.
- `groups` (optional, default: `["default"]`): The groups of optional dependencies or dev dependency groups of PDM to sync with.
- `format` (optional, default: `"requirements"`): The format of the exported file, same as the `--format` option to the `pdm export` command.
  Only `requirements` and `setuppy` are supported.
- `without-hashes` (optional, default: `false`): Whether to remove the hashes from the exported file. Only applicable to `requirements` format.
- `pyproject` (optional, default: `false`): Whether to read dependencies from `pyproject.toml` (see `--pyproject` option to the `pdm export` command).
