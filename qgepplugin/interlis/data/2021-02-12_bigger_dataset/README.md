Test dataset provided by Stefan.

He is able to import it using his scripts and ILI2PG 4.4.6 snapshot.

Here (with 4.4.6) it fails with ili2pg :
```
Error: Object pz0fczksuq0kxh4b at (line 196,col 63)
Error:   ERROR: value too long for type character varying(20)
Error: failed to query SIA405_ABWASSER_2015_LV95.SIA405_Abwasser.Organisation
Error:   ERROR: current transaction is aborted, commands ignored until end of transaction block
Error:     ERROR: value too long for type character varying(20)
java.lang.NullPointerException
```

After changing the .ili files (regex replacing `TEXT\*([0-9]+);` by `TEXT*255` ,still easier than replace in the .xtf :-) ), ili2pg works (but our import fails :-( ).
