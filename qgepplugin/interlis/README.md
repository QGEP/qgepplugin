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

## Use case 1 : import Wincan-generated xtf data into QGEP

```
python -m interlis --force_recreate qgep import interlis\data\test_without_abwasserbauwerkref.xtf
```
