# IMS

**IMS (Install My Shit)** is a Python-based package management and system restoration tool for Arch-based Linux distributions, made by nmesoma.

IMS inventories and classifies explicitly installed packages, audits an existing system against a curated manifest, plans installations, and installs missing packages to help rebuild a Linux environment.

## Features

- Validate TOML package manifests.
- Classify explicitly installed packages into suggested categories.
- Audit installed packages against a curated manifest.
- Generate a plan identifying missing packages.
- Install missing packages using `pacman`.
- Restore a broader package selection using an expanded restoration manifest.
- Skip packages that are already installed.
- Request confirmation before installing packages.
- Require additional confirmation when restoration includes designated system-critical packages.
- Return meaningful exit codes when operations fail.

## Requirements

- Python 3.11 or newer.
- An Arch-based Linux distribution.
- `pacman`.
- `sudo` privileges for package installation.
- Package inventory snapshots in `~/savefiles/` for classification and auditing.

Python 3.11 or newer is required for the standard-library `tomllib` module.

## Usage

Run commands from the IMS project directory.

### Validate the manifest

```bash
python ims.py validate
```

Checks the curated package manifest for invalid categories, malformed entries, and duplicate packages.

### Classify packages

```bash
python ims.py classify
```

Generates suggested package classifications from the available package inventory. Review the generated suggestions before adopting them.

### Audit the system

```bash
python ims.py audit
```

Compares the package inventory against the curated manifest.

### Plan an installation

```bash
python ims.py plan
```

Displays which curated packages are missing from the current system without installing them.

### Normal installation

```bash
python ims.py install
```

Validates the curated manifest, identifies missing packages, displays the proposed installation list, and requests confirmation before invoking `pacman`.

### System restoration

```bash
python ims.py restore
```

Uses the expanded restoration manifest at `config/packages-review.toml` to identify and install missing packages.

If designated system-critical packages are missing, IMS requires an additional confirmation before proceeding. Review the package list carefully before approving restoration.

## Package manifests

### Curated manifest

The curated manifest is located at `config/packages.toml`.

Packages are organized into categories:

```toml
[development]
packages = [
    "git",
    "python",
    "python-pip",
]
```

This manifest defines the packages used by normal installation and planning operations.

### Restoration manifest

The expanded restoration manifest is located at `config/packages-review.toml`.

It contains suggested classifications generated from the explicitly installed packages recorded on the source system. These classifications must be reviewed before relying on them for restoration.

The restoration manifest is broader than the curated manifest and may contain packages specific to the original machine.

## Package inventories

IMS uses package inventory snapshots stored in `~/savefiles/`:

- `packages-explicit.txt`
- `packages-dependencies.txt`
- `packages-foreign.txt`

Refresh these files from the relevant system before running classification or auditing operations.

Installation planning queries the installed package names directly through `pacman`, rather than relying on a saved inventory snapshot.

## Safety and limitations

- IMS validates manifests before proceeding with installation.
- Already-installed packages are excluded from the installation plan.
- Installation requires explicit user confirmation.
- Restoration requires additional confirmation when designated critical packages are missing.
- IMS does not automatically configure repositories, install AUR helpers, restore personal files, or reproduce every operating-system setting.
- Packages unavailable in the configured repositories may fail to install.
- Package availability and names can change over time.
- Restoring packages does not guarantee an identical system configuration.

Review restoration manifests and installation lists before approving changes. Keep backups of important files and system configuration before rebuilding a machine.

## Testing

Run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## Project status

IMS is an experimental personal project. Its core package validation, inventory, planning, installation, and restoration workflows are implemented. Restoration results depend on the target system, configured repositories, and the accuracy of the selected manifest. And most of the packages are what i personally would want to use in every fresh install of an arch based distro.

Made by nmesoma.
