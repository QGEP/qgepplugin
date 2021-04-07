from QgepSwmm import QgepSwmm
qs = QgepSwmm(
'titre',
'pg_qgep_gruner',
None,
None,
None,
'C:/temp/gruner/summary.rpt',
None,
None,
)

qs.import_results('test simulation')