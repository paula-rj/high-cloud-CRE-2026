# high-cloud-CRE-2026

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

This repository contains the code, data-processing workflows, and analysis notebook associated with the article:

**Observational quantification of high cloud radiative sensitivity to aerosol in the Tropical Pacific**

> **Romero Jure et al. (2026)**  
> Journal of Geosciences Research: Atmosphere  
> Pre-print:


## Installation

### Option 1 — Conda 

```bash
conda env create -f environment.yml
conda activate high-cloud-cre
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

The analysis and workflows for producing the figures in the article can be found at the `analysis.ipynb` notebook.
The methods used in this notebook and explained in the Methods section of the article can be found at `methods.py`.

---

## Citation

If you use this repository, please cite:

Software citation:

```bibtex
@software{high-cloud-cre2026,
  author = {P. Romero Jure},
  title = {High Cloud CRE 2026},
  year = {2026},
  doi = {10.xxxx/zenodo.xxxxx}
}
```

If you are using any figures or information from the article (also shown at the `analysis.ipynb` notebook) please use the pre-print citation:

```bibtex
@article{romerojure2026,
  title={Observational quantification of high cloud radiative sensitivity to aerosol in the Tropical Pacific},
  author={Author, A. and Collaborator, B.},
  journal={Journal Name},
  year={2026},
  doi={10.xxxx/xxxxx}
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
