from QgepSwmm import QgepSwmm
with QgepSwmm(
'titre',
'pg_qgep_gruner',
None,
'C:/temp/gruner/out/input.inp',
None,
'C:/temp/gruner/out/summary.rpt',
'C:/Program Files (x86)/EPA SWMM 5.1.013/swmm5.exe',
None,
None,
) as qs:

    #qs.execute_swmm()
    #qs.import_results('SWMM simulation, T100, current')
    dic = qs.extract_time_series_indexes()
    #data = qs.extract_result_lines('<<< Link CHamtKnv00006748 >>>')
    print (dic)