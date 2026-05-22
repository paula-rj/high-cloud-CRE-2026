# high-cloud-CRE-2026

> Observational quantification of high cloud radiative sensitivity to aerosol in the Tropical Pacific

[![DOI](https://img.shields.io/badge/DOI-10.xxxx%2Fxxxxx-blue)](https://doi.org/xx.xxxx/xxxxx)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview

This repository contains the code, data-processing workflows, and analysis notebooks associated with:

> **Romero Jure et al. (2026)**  
> *Observational quantification of high cloud radiative sensitivity to aerosol in the Tropical Pacific*  
> Journal of Geosciendce Research: Atmosphere  
> Pre-print:

### Plain Language summary



> This repository reproduces the experiments, figures, and statistical analyses presented in the manuscript.

---

## Installation

### Option 1 — Conda 

```bash
conda env create -f environment.yml
conda activate project-name
```

### Option 2 — pip

```bash
pip install -r requirements.txt
```

### Launch Jupyter

```bash
jupyter lab
```

---

## Data Availability

The following datasets are used in this project:

| Dataset |  Access |
|---|---|
| CERES FBCT | [CERES data](https://ceres.larc.nasa.gov/data/#fluxbycldtyp-level-3) |
| GISTEMP |  https://example.org/datasetB |
| MODIS AOD | Subset of variable used available in `data/`. |
| MERRA2 | |
---

## Running the Analysis

### Reproduce all results

```bash
python run_analysis.py
```

### Run notebooks

Recommended notebook order:

1. `01_preprocessing.ipynb`
2. `02_analysis.ipynb`
3. `03_figures.ipynb`

---

## Citation

If you use this repository, please cite:

```bibtex
@article{author2026paper,
  title={Paper Title},
  author={Author, A. and Collaborator, B.},
  journal={Journal Name},
  year={2026},
  doi={10.xxxx/xxxxx}
}
```

Software citation:

```bibtex
@software{project2026,
  author = {Author Name},
  title = {Project Name},
  year = {2026},
  doi = {10.xxxx/zenodo.xxxxx}
}
```

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

## Contact

**Paula Romero Jure**  
University of Leeds
eepvrj@leeds.ac.uk

For questions, bug reports, or collaboration inquiries, please open an issue or contact the main author directly.
