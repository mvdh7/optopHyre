# optopHyre

![Tests](https://github.com/mvdh7/optopHyre/workflows/Tests/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/optopHyre.svg?style=popout)](https://pypi.org/project/optopHyre/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/optopHyre.svg)](https://anaconda.org/conda-forge/optopHyre)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.13885218-informational)](https://doi.org/10.5281/zenodo.13885218)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## General

  - [ ] Write numpy-style docstrings throughout

## `lag`

  - [ ] Create new sub-module for lag analysis.
  - [ ] Find optimised value for the lag --- with multiple methods!

## `merge`

  - [ ] Smoothing / moving average before interpolating in `ship_to_optode`
  - [ ] Preparing data ready for `optode_to_ship`
  - [ ] Calculating datenum
  - [ ] Dealing with time zones
  - [ ] Converting from pandas to numpy and back again

## `plot`

  - [ ] Check smoothing applied (`ship_to_optode`)
  - [ ] Check interpolations (`ship_to_optode`)
  - [ ] Check matching (`optode_to_ship`)
  - [ ] Check lag correction

## `read`



## `uncertainty`

Make functions that take numpy arrays as inputs and outputs

  - [ ] Bootstrapping
  - [ ] Kriging

## Packaging
