# IMS

**IMS** is a Python-based Linux package inventory, classification, auditing, and restoration-planning tool for Arch-based systems.

It helps document an existing installation, compare installed packages against a curated manifest, and identify packages that would be needed to recreate the intended setup.

## Features

- Validate a TOML package manifest.
- Classify explicitly installed packages into suggested categories.
- Audit installed packages against the curated manifest.
- Generate a restoration plan for missing curated packages.
- Run operations through a unified command-line interface.
- Operate without installing, removing, or updating packages.

## Requirements

- Python 3.11 or newer
- Arch-based Linux distribution
- `pacman`
- Package inventory files in `~/savefiles/` for classification and auditing

Python 3.11 or newer is required for the standard-library `tomllib` module.

## Usage

Run commands from the IMS project directory.

```bash
python ims.py validate
python ims.py classify
python ims.py audit
python ims.py plan
```

### Manifest

The curated manifest is located at `config/packages.toml`.

Packages are grouped by category:

```toml
[development]
packages = [
    "git",
    "python",
    "python-pip",
]
```

The generated `config/packages-review.toml` contains suggested classifications and should be reviewed before adopting those suggestions into the curated manifest.

### Package inventories

IMS reads package inventory snapshots from `~/savefiles/`:

- `packages-explicit.txt`
- `packages-dependencies.txt`
- `packages-foreign.txt`

These files should be generated from the target system and refreshed before auditing. The restoration planner queries the installed package names directly using `pacman`.

## Safety

IMS is read-only by default.

The restoration planner identifies missing packages and prints a proposed installation command. It does not execute that command or install packages.

Review all proposed changes before carrying them out manually.

## Testing

Run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## Project status

IMS is an experimental personal project. Package classifications and restoration manifests should be reviewed before being used to rebuild a system.