# ili2QWAT / ili2QGEP prototype

## General usage
```
python -m interlis [-h] [--force_recreate]
                   {qgep,qwat} {export,import} xtf_file

positional arguments:
  {qgep,qwat}
  {export,import}
  xtf_file

optional arguments:
  -h, --help        show this help message and exit
  --force_recreate  Drops and recreate the ili2pg schemas if already existing
```

## Dev

Import scripts templates can be generated using `python -m interlis qwat --gen_tpl; python -m interlis qgep`. This uses the mapping defined in `datamodels/mapping.py` to auto-generate import script templates, that can then be manually merged into the existing scripts.

## Use cases

### A. import Wincan-generated xtf data into QGEP

We recieve data from a TV inspection company as a Wincan exported .xtf file. We want this data loaded into QGEP.

```
python -m interlis --force_recreate qgep import interlis\data\test_without_abwasserbauwerkref.xtf
```
