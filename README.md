# high-cloud-CRE-2026

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/paula-rj/high-cloud-CRE-2026.git/main?urlpath=%2Fdoc%2Ftree%2Fanalysis-high-cloud-cre.ipynb)

This repository contains the code, data-processing workflows, and analysis notebook associated with the article:

**Observational quantification of high cloud radiative sensitivity to aerosol in the Tropical Pacific**

> **Paula Romero Jure, Declan L. Finney, Amanda C. Maycock, Anna Mackie, Ross J. Herbert, and Alan Blyth**  
> Journal of Geosciences Research: Atmosphere  
> Pre-print here:

---

## Citation

Software citation:

If you use this repository, please use the **Cite this repository** tab to the right to copy the citation to your clipboard.

Or copy it on Bibtex format from here

```bibtex
@software{Romero_Jure_high-cloud-CRE-2026,
author = {Romero Jure, Paula},
license = {MIT},
title = {{high-cloud-CRE-2026}},
url = {https://github.com/paula-rj/high-cloud-CRE-2026.git}
}
```

If you are using any figures or information from the article (also shown at the `analysis.ipynb` notebook), please use the pre-print citation

```bibtex
@article{romerojure2026,
  title={Observational quantification of high cloud radiative sensitivity to aerosol in the Tropical Pacific},
  author={Paula Romero Jure and Declan L. Finney and Amanda C. Maycock and Anna Mackie and Ross J. Herbert and Alan Blyth},
  journal={},
  year={2026},
  doi={10.xxxx/xxxxx}
}
```

---
## Running the analysis

1- Download the data (Links on Data Availability below).

2- Clone or install the repository 

3- Create a virtual environment to run it. Here are some options:

### Option 1 — Conda 

```bash
conda env create -f environment.yml
conda activate high-cloud-cre
```

### Option 2 — pip

```bash
python3.12 -m venv high-cloud-cre
source high-cloud-cre/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
This will ensure the correct dependencies are installed to run the analysis notebook. 

4- Update the kernel on the Jupyter notebook.
```bash
python -m ipykernel install --user --name=high-cloud-cre --display-name "Python (high-cloud-cre)"
```
5- Restart the kernel and choose Python (high-cloud-cre) from the kernel options.

---

## Data Availability

The following datasets are used in this project:

| Dataset |  Access link | DOI | Related article |
|---|---|---|---|
| CERES Flux By Cloud Type (FBCT) | [CERES data](https://ceres.larc.nasa.gov/data/#fluxbycldtyp-level-3) | 10.5067/Terra-Aqua/CERES/FLUXBYCLDTYP-MONTH L3.004A | |
| GISTEMP GMST |  [NASA Goddard Institute for Space Studies](https://data.giss.nasa.gov/gistemp/) | | |
| Collection 6 MODIS aerosol products | Subset of variable "Aerosol Optical Depth Average Ocean Quality Assured Mean of Means", used in this analysis, is conveniently available in the `data/` directory of this repository. MYD08 is available from [Google Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MYD08_M3)| 10.5067/MODIS/561MYD08 M3.061| |
| MERRA2 | [Global Modeling and Assimilation Office (GMAO)](https://cmr.earthdata.nasa.gov/search/concepts/C1276812824-GES_DISC.html) | | |
---

## Running the Analysis

The analysis and workflows for producing the figures in the article can be found at the `analysis.ipynb` notebook.

You'll need to download the data from the links provided above. 

The methods used in this notebook, as explained in the Methods section of the article, can be found in `methods.py`.


---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

## Contact

**Paula Romero Jure**  
University of Leeds
eepvrj@leeds.ac.uk

For questions, bug reports, or collaboration inquiries, please open an issue or contact the main author directly.
