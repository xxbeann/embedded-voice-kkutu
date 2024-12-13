# Voice KKuTu

Voice KKuTu - Team Project for Embedded Software Lecture

## Getting Started

[`rye`](https://rye.astral.sh) is required for run this project easily.

```sh
# Fetch KKuTu Repository
git module init
git module update

# Install dependencies
rye sync

# Convert word database from KKuTu DB
rye run convert

# Install pre commit script for linting
rye run pre-commit
```

If below commands are not executed sucessfully, Try `rye sync` first.

**Commands**
```
rye run app
rye run convert
rye run clean
rye run black
rye run pre-commit
```

### Convert word data from KKuTu DB
This repository contains KKuTu repository as submodule.  

Word data for KKuTu server can be migrated for this project with converting script.

```sh
git submodule init
git submodule update
rye run convert
```
