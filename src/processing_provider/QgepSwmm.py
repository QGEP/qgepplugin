# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGEP-swmm processing provider
                              -------------------
        begin                : 07.2019
        copyright            : (C) 2019 by ig-group.ch
        email                : timothee.produit@ig-group.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import psycopg2
import codecs
import subprocess
import os


class QgepSwmm:

    def __init__(self, title, service, inpfile, inptemplate, outfile, logfile, binfile, db_model_path):
        """
        Initiate QgepSwmm

        Parameters:
        title (string): Title of the simulation
        service (string): name of the service to be used to connect to the QGEP database
        inpfile (path): path of the INP file (input file for swmm)
        inptemplate (path): path of the INP file which store simulations parameters
        outfile (path): path of the OUT file which contains swmm results
        logfile (path): path of the log file which contains swmm log
        db_model_path (path): path of the folder which contains the db model
        """
        self.title = title
        self.service = service
        self.input_file = inpfile
        self.options_template_file = inptemplate
        self.output_file = outfile
        self.log_file = logfile
        self.bin_file = binfile
        self.db_model_path = db_model_path

    def create_swmm_schema(self):
        """
        Create QGEP-SWMM schema
        """

        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_create_schema.sql"), "r").read())
        con.commit()

        return

    def create_swmm_views(self):
        """
        Create QGEP-SWMM views
        """

        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_conduits.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_junctions.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_outfalls.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_pumps.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_storages.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_subcatchments.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_xsections.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_losses.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_coordinates.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_vertices.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_polygons.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_tags.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_aquifers.sql"), "r").read())
        cur.execute(open(os.path.join(self.db_model_path, "vw_swmm_landuses.sql"), "r").read())
        con.commit()

        return

    def delete_swmm_tables(self):
        """
        Delete swmm tables
        """
        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.conduits")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.junctions")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.outfalls")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.pumps")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.storages")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.subcatchments")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.subareas")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.infiltration")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.xsections")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.losses")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.coordinates")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.vertices")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.polygons")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.raingages")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.tags")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.aquifers")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.landuses")
        cur.execute("DROP TABLE IF EXISTS qgep_swmm.coverages")
        con.commit()
        return

    def create_fill_swmm_tables(self):
        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        cur.execute("CREATE TABLE qgep_swmm.conduits AS TABLE qgep_swmm.vw_conduits")
        cur.execute("CREATE TABLE qgep_swmm.junctions AS TABLE qgep_swmm.vw_junctions")
        cur.execute("CREATE TABLE qgep_swmm.outfalls AS TABLE qgep_swmm.vw_outfalls")
        cur.execute("CREATE TABLE qgep_swmm.pumps AS TABLE qgep_swmm.vw_pumps")
        cur.execute("CREATE TABLE qgep_swmm.storage AS TABLE qgep_swmm.vw_storages")
        cur.execute("CREATE TABLE qgep_swmm.subcatchments AS TABLE qgep_swmm.vw_subcatchments")
        cur.execute("CREATE TABLE qgep_swmm.subareas AS TABLE qgep_swmm.vw_subareas")
        cur.execute("CREATE TABLE qgep_swmm.infiltration AS TABLE qgep_swmm.vw_infiltration")
        cur.execute("CREATE TABLE qgep_swmm.xsections AS TABLE qgep_swmm.vw_xsections")
        cur.execute("CREATE TABLE qgep_swmm.losses AS TABLE qgep_swmm.vw_losses")
        cur.execute("CREATE TABLE qgep_swmm.coordinates AS TABLE qgep_swmm.vw_coordinates")
        cur.execute("CREATE TABLE qgep_swmm.vertices AS TABLE qgep_swmm.vw_vertices")
        cur.execute("CREATE TABLE qgep_swmm.polygons AS TABLE qgep_swmm.vw_polygons")
        cur.execute("CREATE TABLE qgep_swmm.raingages AS TABLE qgep_swmm.vw_raingages")
        cur.execute("CREATE TABLE qgep_swmm.tags AS TABLE qgep_swmm.vw_tags")
        cur.execute("CREATE TABLE qgep_swmm.aquifers AS TABLE qgep_swmm.vw_aquifers")
        cur.execute("CREATE TABLE qgep_swmm.landuses AS TABLE qgep_swmm.vw_landuses")
        cur.execute("CREATE TABLE qgep_swmm.coverages AS TABLE qgep_swmm.vw_coverages")
        con.commit()
        return

    def get_swmm_table(self, table_name):
        """
        Extract data from the swmm views in the database

        Parameters:
        table_name (string): Name of the view or tablle

        Returns:
        dic: table content
        array: table attributes

        """

        # Connects to service and get data and attributes from tableName
        con = psycopg2.connect(service=self.service)
        cur = con.cursor()
        try:
            cur.execute('select * from qgep_swmm.{table_name}'.format(table_name=table_name))
        except psycopg2.ProgrammingError:
            print('Table %s doesnt exists' % table_name)
            return None, None
        data = cur.fetchall()
        attributes = [desc[0] for desc in cur.description]

        return data, attributes

    def swmm_table(self, table_name):
        """
        Create swmm table

        Parameters:
        table_name (string): Name of the swmm section

        Returns:
        String: table content

        """

        # Create commented line which contains the field names
        fields = ""
        data, attributes = self.get_swmm_table(table_name)
        if data is not None:
            for i, field in enumerate(attributes):
                # Does not write values stored in columns descriptions, tags and geom
                if field not in ('description', 'tag', 'geom'):
                    fields += field + "\t"

            # Create input paragraph
            tbl = u'[' + table_name + ']\n'\
                ';;' + fields + '\n'
            for feature in data:
                for i, v in enumerate(feature):
                    # Write description
                    if attributes[i] == 'description' and v is not None:
                        tbl += ';'
                        tbl += str(v)
                        tbl += '\n'

                for i, v in enumerate(feature):
                    # Does not write values stored in columns descriptions, tags and geom
                    if attributes[i] not in ('description', 'tag', 'geom'):
                        if v is not None:
                            tbl += str(v) + '\t'
                        else:
                            tbl += '\t'
                tbl += '\n'
            tbl += '\n'
            return tbl
        else:
            return '\n'

    def copy_parameters_from_template(self, parameter_name):
        """
        Create swmm table from the template

        Parameters:
        parameter_name (string): Name of the swmm section to be copied

        Returns:
        String: section content

        """
        # Read template
        options_template = open(self.options_template_file, 'r').read()
        # Find and extract options
        index_start = options_template.find('[%s]' % parameter_name)
        if index_start == -1:
            # The balise options is not found
            print('There is no [%s] in the template file' % parameter_name)
            return ''
        else:
            # Search for the next opening bracket
            index_stop = options_template[index_start + 1:].find('[')
            if index_stop == -1:
                # Copies text until the end of the file
                index_stop = len(options_template)
                option_text = options_template[index_start:index_stop] + '\n\n'
            else:
                index_stop = index_start + 1 + index_stop
                option_text = options_template[index_start:index_stop]
            return option_text

    def write_input(self):
        """
        Write the swmm input file

        """

        # From qgis swmm
        filename = self.input_file

        with codecs.open(filename, 'w', encoding='utf-8') as f:

            # Title / Notes
            # --------------
            f.write('[TITLE]\n')
            f.write(self.title + '\n\n')

            # Options
            # --------
            f.write(self.copy_parameters_from_template('OPTIONS'))
            f.write(self.copy_parameters_from_template('REPORT'))
            f.write(self.copy_parameters_from_template('FILES'))
            f.write(self.copy_parameters_from_template('EVENTS'))

            # Climatology
            # ------------
            f.write(self.copy_parameters_from_template('HYDROGRAPHS'))
            f.write(self.copy_parameters_from_template('EVAPORATION'))
            f.write(self.copy_parameters_from_template('TEMPERATURE'))

            # Hydrology
            # ----------
            f.write(self.swmm_table('RAINGAGES'))
            f.write(self.swmm_table('SUBCATCHMENTS'))
            f.write(self.swmm_table('SUBAREAS'))
            f.write(self.swmm_table('AQUIFERS'))
            f.write(self.swmm_table('INFILTRATION'))
            f.write(self.swmm_table('POLYGONS'))

            f.write(self.copy_parameters_from_template('INFLOWS'))
            f.write(self.copy_parameters_from_template('GROUNDWATER'))
            f.write(self.copy_parameters_from_template('SNOWPACKS'))
            f.write(self.copy_parameters_from_template('HYDROGAPHS'))
            f.write(self.copy_parameters_from_template('LID_CONTROLS'))
            f.write(self.copy_parameters_from_template('LID_USAGE'))

            # Hydraulics: nodes
            # ------------------
            f.write(self.swmm_table('JUNCTIONS'))
            # Create default junction to avoid errors
            f.write('default_qgep_node\t0\t0\n\n')
            f.write(self.swmm_table('OUTFALLS'))
            f.write(self.swmm_table('STORAGE'))
            f.write(self.swmm_table('COORDINATES'))

            f.write(self.copy_parameters_from_template('DIVIDERS'))

            # Hydraulics: links
            # ------------------
            f.write(self.swmm_table('CONDUITS'))
            f.write(self.swmm_table('PUMPS'))
            f.write(self.copy_parameters_from_template('ORIFICES'))
            f.write(self.copy_parameters_from_template('WEIRS'))
            f.write(self.copy_parameters_from_template('OUTLETS'))
            f.write(self.swmm_table('XSECTIONS'))
            f.write(self.swmm_table('LOSSES'))
            f.write(self.swmm_table('VERTICES'))

            f.write(self.copy_parameters_from_template('TRANSECTS'))
            f.write(self.copy_parameters_from_template('CONTROLS'))

            # Quality
            # --------
            f.write(self.swmm_table('LANDUSES'))
            f.write(self.swmm_table('COVERAGES'))

            f.write(self.copy_parameters_from_template('POLLUTANTS'))
            f.write(self.copy_parameters_from_template('BUILDUP'))
            f.write(self.copy_parameters_from_template('WASHOFF'))
            f.write(self.copy_parameters_from_template('TREATMENT'))
            f.write(self.copy_parameters_from_template('DWF'))
            f.write(self.copy_parameters_from_template('RDII'))
            f.write(self.copy_parameters_from_template('LOADINGS'))

            # Curves
            # -------
            f.write(self.copy_parameters_from_template('CURVES'))

            # Time series
            # ------------
            f.write(self.copy_parameters_from_template('TIMESERIES'))

            # Time patterns
            # --------------
            f.write(self.copy_parameters_from_template('PATTERNS'))

            # Map labels
            # -----------
            f.write(self.copy_parameters_from_template('LABELS'))

            f.write(self.swmm_table('TAGS'))

        return

    def extract_result_lines(self, table_title):
        """
        Extract result data from swmm output file

        Parameters:
        table_title (string): Name of the section to be extracted

        Returns:
        Array of array: Extracted computed values

        """

        o = codecs.open(self.output_file, 'r', encoding='utf-8')
        line = o.readline()
        no_line = 0
        lines = []
        title_found = False
        end_table_found = False
        while line:
            line = line.rstrip()
            # Search for the table title
            if line.find(table_title) != -1:
                title_found = True
                line_after_title = 0

            if title_found and line_after_title > 7 and line == '':
                end_table_found = True

            if title_found and end_table_found is False and line_after_title > 7:
                lines.append(line.split())

            if title_found:
                line_after_title += 1

            no_line += 1
            line = o.readline()

        return lines

    def extract_node_depth_summary(self):
        """
        Extract node depth result data from swmm output file

        Returns:
        dic: Extracted computed values

        """

        data = self.extract_result_lines('Node Depth Summary')
        result = []
        for d in data:
            curres = {}
            curres['id'] = d[0]
            curres['type'] = d[1]
            curres['average_depth'] = d[2]
            curres['maximum_depth'] = d[3]
            curres['maximum_hgl'] = d[4]
            curres['time_max_day'] = d[5]
            curres['time_max_time'] = d[6]
            curres['reported_max_depth'] = d[7]
            result.append(curres)
        return result

    def extract_link_flow_summary(self):
        """
        Extract link flow result data from swmm output file

        Returns:
        dic: Extracted computed values

        """

        data = self.extract_result_lines('Link Flow Summary')
        result = []
        for d in data:

            curres = {}
            curres['id'] = d[0]
            curres['type'] = d[1]
            curres['maximum_flow'] = d[2]
            curres['time_max_day'] = d[3]
            curres['time_max_time'] = d[4]
            if d[1] == 'CONDUIT':
                curres['maximum_velocity'] = d[5]
                curres['max_over_full_flow'] = d[6]
                curres['max_over_full_depth'] = d[7]
            elif d[1] == 'PUMP':
                curres['max_over_full_flow'] = d[5]
                curres['maximum_velocity'] = None
                curres['max_over_full_depth'] = None

            result.append(curres)
        return result

    def extract_cross_section_summary(self):
        """
        Extract cross sections result data from swmm output file

        Returns:
        dic: Extracted computed values

        """
        data = self.extract_result_lines('Cross Section Summary')
        result = []
        for d in data:

            curres = {}
            curres['id'] = d[0]
            curres['shape'] = d[1]
            curres['full_depth'] = d[2]
            curres['full_area'] = d[3]
            curres['hyd_rad'] = d[4]
            curres['max_width'] = d[5]
            curres['no_of_barrels'] = d[6]
            curres['full_flow'] = d[7]

            result.append(curres)
        return result

    def execute_swmm(self):
        """
        Execute SWMM

        Parameters:
        dic: Extracted computed values

        """

        command = [self.bin_file, self.input_file, self.log_file, self.output_file]
        print('command', command)
        proc = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        ).stdout

        return proc


# =============================================================================
# Examples to show how theses functions can be used within Python scripts

# TITLE = 'title simulation'
# PGSERVICE = 'pg_qgep_demo_data'
# INPFILE = '\\qgep_swmm\\input\\qgep_swmm.inp'
# INPTEMPLATE = '\\qgep_swmm\\simulation_parameters\\default_qgep_swmm_parameters.inp'
# OUTFILE = '\\qgep_swmm\\output\\swmm_test.out'
# LOGFILE = '\\qgep_swmm\\output\\log.out'
# BINFILE = 'C:\\Program Files (x86)\\EPA SWMM 5.1.013\\swmm5'
# DBMODEL = '\\qgep_swmm\\02_datamodel\\swmm_views'
#
# qs = QgepSwmm(TITLE, PGSERVICE, INPFILE, INPTEMPLATE, OUTFILE, LOGFILE, BINFILE, DBMODEL)
# qs.create_swmm_schema()
# qs.create_swmm_views()
# qs.delete_swmm_tables()
# qs.create_fill_swmm_tables()
# qs.execute_swmm()
# =============================================================================
