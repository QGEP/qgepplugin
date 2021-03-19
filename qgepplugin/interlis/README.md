# ili2QWAT / ili2QGEP prototype

## General usage

Import/export
```
usage: python -m qgepplugin.interlis io [-h] [--recreate_schema] [--skip_validation]
                                        [--import_xtf IMPORT_XTF | --export_xtf EXPORT_XTF]
                                        {qgep,qwat}

positional arguments:
  {qgep,qwat}           datamodel

optional arguments:
  -h, --help            show this help message and exit
  --recreate_schema     drops schema and reruns ili2pg importschema
  --skip_validation     skips running ilivalidator on input/output xtf
                        (required to import invalid files, invalid outputs are
                        still generated)
  --import_xtf IMPORT_XTF
                        input file
  --export_xtf EXPORT_XTF
                        output file
```

Setting up a test database
```
usage: python -m qgepplugin.interlis setupdb [-h] {empty,full,subset}

positional arguments:
  {empty,full,subset}  type

optional arguments:
  -h, --help           show this help message and exit
```

## Using in QGIS

```
# install python3-pip using OSGeo4W installer
# in the OSGeo4W shell
pip install sqlalchemy geoalchemy2 psycopg2
```

## Dev

Import scripts templates can be generated using `python -m interlis qwat --gen_tpl; python -m interlis qgep --gen_tpl`. This uses the mapping defined in `datamodels/mapping.py` to auto-generate import script templates, that can then be manually merged into the existing scripts.

## Use cases

### A. import Wincan-generated xtf data into QGEP

We recieve data from a TV inspection company as a Wincan exported .xtf file. We want this data loaded into QGEP.

```
python -m interlis --recreate_schema --import_xtf interlis\data\test_without_abwasserbauwerkref.xtf qgep
```

## Code use

```python
import interlis
from sqlalchemy.orm import Session
from interlis.qgep.model_qgep import QGEP

engine = interlis.utils.sqlalchemy.create_engine()
session = Session(engine, autocommit=False, autoflush=False)

examination = session.query(QGEP.examination).first()
dir(examination)
```
