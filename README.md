# sofa_verification

A small collection of files for checking the validity and consistency of
the SOFA conventions from [API_MO](https://github.com/sofacoustics/API_MO)
in the folder `consistency_of_conventions` and the validity of SOFA files
downloaded from [sofa conventions](https://sofaconventions.org/mediawiki/index.php/Files)
in the folder `validata_sofa_files`. The folder `plotting_examples` contains
examples for plotting head-related transfer functions using [pyfar](https://pyfar.org).

## Setup

To create the environment to reproduce the paper, run:

``` $
conda env create -f environment.yml --prefix ./env/2022_jaes_sofar_appendix/
```

and activate using:

``` $
conda activate ./env/2022_jaes_sofar_appendix/
```

The specific environment (potentially very OS specific) can be exported

``` $
conda env export --prefix ./env/2022_jaes_sofar_appendix/ --file exact_environment.yml
```

and updated:

``` $
conda env update --prefix ./env/2022_jaes_sofar_appendix/ --file exact_environment.yml  --prune
```
