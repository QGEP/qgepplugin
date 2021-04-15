from QgepSwmm import QgepSwmm
with QgepSwmm(
'titre',
'pg_qgep_gruner',
'current',
'C:/temp/gruner/out/input.inp',
'C:/temp/gruner/out/swmm_template.inp',
'C:/temp/gruner/out/summary.rpt',
'C:/Program Files (x86)/EPA SWMM 5.1.013/swmm5.exe',
None,
) as qs:

    #qs.execute_swmm()
    #qs.import_summary('SWMM simulation, T100, current')
    qs.import_full_results('SWMM simulation, T100, current')
    #data = qs.extract_result_lines('<<< Link CHamtKnv00006748 >>>')
    #print (dic)