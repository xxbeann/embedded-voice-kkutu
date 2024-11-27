# Voice KKuTu

Voice KKuTu - Team Project for Embedded Software Lecture

## Getting Started

[`rye`](https://rye.astral.sh) is required for run this project easily.

```sh
rye sync
```

**Commands**
```
rye run app
rye run convert
rye run clean
```

### Convert word data from KKuTu DB
This repository contains KKuTu repository as submodule.  

Word data for KKuTu server can be migrated for this project with converting script.

```sh
git submodule update
rye convert
```
