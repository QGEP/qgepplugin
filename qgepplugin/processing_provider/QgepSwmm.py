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
from datetime import datetime, timedelta

MEASURING_POINT_KIND = 'SWMM Simulation' #[TO VALIDATE]

SWMM_OUTPUT_PARAMETERS  = {}
SWMM_OUTPUT_PARAMETERS['average_depth'] = {'recorded': True, 'dimension': 'm', 'qgep_measurement_type': 5734}
SWMM_OUTPUT_PARAMETERS['maximum_depth'] = {'recorded': True, 'dimension': 'm', 'qgep_measurement_type': 5734}
SWMM_OUTPUT_PARAMETERS['maximum_hgl'] = {'recorded': True, 'dimension': 'm', 'qgep_measurement_type': 5734}
SWMM_OUTPUT_PARAMETERS['reported_max_depth'] = {'recorded': True, 'dimension': 'm', 'qgep_measurement_type': 5734}
SWMM_OUTPUT_PARAMETERS['maximum_flow'] = {'recorded': True, 'dimension': 'l/s', 'qgep_measurement_type': 5732}
SWMM_OUTPUT_PARAMETERS['maximum_velocity'] = {'recorded': True, 'dimension': 'm/s', 'qgep_measurement_type': 5732}
SWMM_OUTPUT_PARAMETERS['max_over_full_flow'] = {'recorded': True, 'dimension': '-', 'qgep_measurement_type': 5732}
SWMM_OUTPUT_PARAMETERS['max_over_full_depth'] = {'recorded': True, 'dimension': '-', 'qgep_measurement_type': 5734}

NON_PHYSICAL_REM = 'Non-physical point which materializes swmm simulations'

class QgepSwmm:

    def __init__(self, title, service, state, inpfile, inptemplate, outfile, binfile, db_model_path, feedback):
        """
        Initiate QgepSwmm

        Parameters:
        title (string): Title of the simulation
        service (string): name of the service to be used to connect to the QGEP database
        state (string): state for which the network is extracted (current or planned)
        inpfile (path): path of the INP file (input file for swmm)
        inptemplate (path): path of the INP file which store simulations parameters
        outfile (path): path of the OUT file which contains swmm results
        binfile (path): path of the swmm executable
        db_model_path (path): path of the folder which contains the db model
        """
        self.title = title
        self.service = service
        self.input_file = inpfile
        self.options_template_file = inptemplate
        self.output_file = outfile
        self.bin_file = binfile
        self.db_model_path = db_model_path
        self.feedback = feedback
        self.state = state


    def __enter__(self):
        if self.service is not None:
            self.con = psycopg2.connect(service=self.service)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.service is not None:
            del self.con

    def get_swmm_table(self, table_name, state, ws):
        """
        Extract data from the swmm views in the database

        Parameters:
        table_name (string): Name of the view or table
        state (string): current or planned
        ws (boolean): if the origin table is a wastewater structure

        Returns:
        dic: table content
        array: table attributes

        """

        # Connects to service and get data and attributes from tableName
        #con = psycopg2.connect(service=self.service)
        cur = self.con.cursor()
        if (state == 'planned' and ws is True) or (state is None):
            sql = 'select * from qgep_swmm.vw_{table_name}'.format(table_name=table_name)
        else:
            sql = """
            select * from qgep_swmm.vw_{table_name}
            where state = '{state}'
            """.format(table_name=table_name, state=state)

        try:
            cur.execute(sql)
        except psycopg2.ProgrammingError:
            self.feedback.reportError('Table vw_{table_name} doesnt exists'.format(table_name=table_name))
            return None, None
        self.feedback.pushInfo('Process vw_{table_name}'.format(table_name=table_name))
        data = cur.fetchall()
        attributes = [desc[0] for desc in cur.description]
        del cur

        return data, attributes

    def swmm_table(self, table_name, state=None, ws=False):
        """
        Write swmm objects extracted from QGEP in swmm input file. Selects according
        to the state planned or current. If the object is a qgep wastewater structure
        when the state is "planned" both "planned" and "operational" wastewater structures are selected

        Parameters:
        table_name (string): Name of the swmm section
        state (string): current or planned
        ws (boolean): if the origin table is a wastewater structure

        Returns:
        String: table content

        """

        # Create commented line which contains the field names
        fields = ""
        data, attributes = self.get_swmm_table(table_name, state, ws)
        if data is not None:
            for i, field in enumerate(attributes):
                # Does not write values stored in columns descriptions, tags and geom
                if field not in ('description', 'tag', 'geom', 'state'):
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
                    if attributes[i] not in ('description', 'tag', 'geom', 'state'):
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
        Write swmm objects extracted from template in swmm input file

        Parameters:
        parameter_name (string): Name of the swmm section to be copied

        Returns:
        String: section content

        """
        # Read template
        options_template = open(self.options_template_file, 'r').read()
        # Find and extract options
        index_start = options_template.find('[{parameter_name}]'.format(parameter_name=parameter_name))
        if index_start == -1:
            # The balise options is not found
            self.feedback.pushInfo('There is no {parameter_name} in the template file'.format(parameter_name=parameter_name))
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
        state = self.state

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
            self.feedback.setProgress(5)
            f.write(self.swmm_table('RAINGAGES', state))
            self.feedback.setProgress(10)
            f.write(self.swmm_table('SUBCATCHMENTS', state))
            self.feedback.setProgress(15)
            f.write(self.swmm_table('SUBAREAS', state))
            self.feedback.setProgress(20)
            f.write(self.swmm_table('AQUIFERS'))
            self.feedback.setProgress(25)
            f.write(self.swmm_table('INFILTRATION', state))
            self.feedback.setProgress(30)
            f.write(self.swmm_table('POLYGONS'))

            f.write(self.copy_parameters_from_template('GROUNDWATER'))
            f.write(self.copy_parameters_from_template('SNOWPACKS'))
            f.write(self.copy_parameters_from_template('HYDROGAPHS'))
            f.write(self.copy_parameters_from_template('LID_CONTROLS'))
            f.write(self.copy_parameters_from_template('LID_USAGE'))

            # Hydraulics: nodes
            # ------------------
            self.feedback.setProgress(35)
            f.write(self.swmm_table('JUNCTIONS', state, ws=True))
            self.feedback.setProgress(40)
            f.write(self.swmm_table('OUTFALLS', state, ws=True))
            self.feedback.setProgress(45)
            f.write(self.swmm_table('STORAGES', state, ws=True))
            self.feedback.setProgress(50)
            f.write(self.swmm_table('COORDINATES'))
            self.feedback.setProgress(55)
            f.write(self.swmm_table('DWF', state))

            f.write(self.copy_parameters_from_template('INFLOWS'))
            f.write(self.copy_parameters_from_template('DIVIDERS'))

            # Hydraulics: links
            # ------------------
            self.feedback.setProgress(60)
            f.write(self.swmm_table('CONDUITS', state, ws=True))
            self.feedback.setProgress(65)
            f.write(self.swmm_table('LOSSES', state, ws=True))
            self.feedback.setProgress(70)
            f.write(self.swmm_table('PUMPS', state, ws=True))
            f.write(self.copy_parameters_from_template('ORIFICES'))
            f.write(self.copy_parameters_from_template('WEIRS'))
            f.write(self.copy_parameters_from_template('OUTLETS'))
            self.feedback.setProgress(75)
            f.write(self.swmm_table('XSECTIONS', state, ws=True))
            self.feedback.setProgress(80)
            f.write(self.swmm_table('LOSSES', state, ws=True))
            self.feedback.setProgress(85)
            f.write(self.swmm_table('VERTICES'))

            f.write(self.copy_parameters_from_template('TRANSECTS'))
            f.write(self.copy_parameters_from_template('CONTROLS'))

            # Quality
            # --------
            self.feedback.setProgress(90)
            f.write(self.swmm_table('LANDUSES'))
            self.feedback.setProgress(93)
            f.write(self.swmm_table('COVERAGES'))

            f.write(self.copy_parameters_from_template('POLLUTANTS'))
            f.write(self.copy_parameters_from_template('BUILDUP'))
            f.write(self.copy_parameters_from_template('WASHOFF'))
            f.write(self.copy_parameters_from_template('TREATMENT'))
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
            self.feedback.setProgress(96)
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

    def execute_swmm(self):
        """
        Execute SWMM

        Parameters:
        dic: Extracted computed values

        """

        command = [self.bin_file, self.input_file, self.output_file]
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

    def get_analysis_option(self, parameter):
        o = codecs.open(self.output_file, 'r', encoding='utf-8')
        line = o.readline()
        while line:
            line = line.rstrip()
            # Search for the analyis option
            if line.find(parameter) != -1:
                value = line.split('.')[-1].strip()
            line = o.readline()
        return value

    def convert_to_datetime(self, str_date):
        date = datetime.strptime(str_date, "%d/%m/%Y %H:%M:%S")
        return date


    def import_results(self, sim_description):
        """
        Import the results fro an SWMM output file

        Parameters:
        ws_obj_id (string): wastewater structure object ID

        Returns:
        me_obj_id: measuring point object ID

        """
        
        simulation_start_date = self.convert_to_datetime(self.get_analysis_option('Starting Date'))
        simulation_end_date = self.convert_to_datetime(self.get_analysis_option('Ending Date'))
        simulation_duration = simulation_end_date - simulation_start_date
        measuring_duration = simulation_duration.total_seconds() # TO VALIDATE
        self.feedback.pushInfo('Import nodes results')
        node_summary = self.extract_node_depth_summary()
        self.record_measures(node_summary, simulation_start_date, sim_description, measuring_duration, 'node')
        self.feedback.pushInfo('Import links results')
        link_summary = self.extract_link_flow_summary()
        self.record_measures(link_summary, simulation_start_date, sim_description, measuring_duration, 'link')

        return

    def record_measures(self, data, simulation_start_date, sim_description, measuring_duration, obj_type):
        nData = len(data)
        # Loop over each line of the node summary
        counter = 0
        for ws in data:
            counter+=1
            if obj_type == 'node':
                self.feedback.setProgress(counter*50/nData)
                mp_obj_id = self.create_measuring_point_node(ws['id'])
            else:
                self.feedback.setProgress(50+counter*50/nData)
                mp_obj_id = self.create_measuring_point_link(ws['id'])
            if mp_obj_id:
                ms_obj_id = self.create_measurement_series(mp_obj_id, sim_description)
                delta = timedelta(
                    days=int(ws['time_max_day']), 
                    hours=int(ws['time_max_time'].split(':')[0]),
                    minutes=int(ws['time_max_time'].split(':')[1]))
                for k in ws.keys():
                    if k in SWMM_OUTPUT_PARAMETERS.keys():
                        if SWMM_OUTPUT_PARAMETERS[k]['recorded']:
                            time = (simulation_start_date + delta).isoformat()
                            self.create_measurement_result(ms_obj_id, SWMM_OUTPUT_PARAMETERS[k]['qgep_measurement_type'],
                            measuring_duration, k, time, ws[k])
        return

    def create_measuring_point_node(self, node_obj_id):

        """
        For a node creates a measuring point or get its id.

        Parameters:
        node_obj_id (string): wastewater node object ID

        Returns:
        me_obj_id: measuring point object ID

        """

        # Connects to service and get data and attributes from tableName
        cur = self.con.cursor()

        # Test if the measuring point exists
        sql = """
        SELECT mp.obj_id
        FROM qgep_od.measuring_point mp
        JOIN qgep_od.wastewater_structure ws on mp.fk_wastewater_structure = ws.obj_id
        WHERE ws.fk_main_wastewater_node = 'CHamtKnv00002027'
        AND kind = '{MEASURING_POINT_KIND}'
        """.format(MEASURING_POINT_KIND=MEASURING_POINT_KIND, node_obj_id=node_obj_id)
    
        cur.execute(sql)
        res = cur.fetchone()

        if res is None:
            # Check if weather the measuring point doesnt exists or the waternode is no
            # Measuring point doesnt exists, must be created
            # 4594 = technical purpose [TO VALIDATE]
            sql = """
            INSERT INTO qgep_od.measuring_point
            (damming_device, identifier, kind, purpose, remark, fk_wastewater_structure)
            SELECT 5721, NULL, '{MEASURING_POINT_KIND}', 4594, '{NON_PHYSICAL_REM}', ws.obj_id 
            FROM qgep_od.wastewater_structure ws
            WHERE fk_main_wastewater_node = '{node_obj_id}'
            RETURNING obj_id
            """.format(MEASURING_POINT_KIND=MEASURING_POINT_KIND, node_obj_id=node_obj_id, NON_PHYSICAL_REM=NON_PHYSICAL_REM)
            try:
                cur.execute(sql)
            except psycopg2.ProgrammingError:
                self.feedback.reportError(str(psycopg2.ProgrammingError), True)
                return None, None
            res = cur.fetchone()
            if res is None:
                mp_obj_id = None
            else:
                mp_obj_id = res[0]
                self.con.commit()
            del cur
        else:
            mp_obj_id = res[0]
        return mp_obj_id

    def create_measuring_point_link(self, reach_obj_id):

        """
        For a node creates a measuring point or get its id.

        Parameters:
        reach_obj_id (string): reach object ID

        Returns:
        me_obj_id: measuring point object ID

        """

        # Connects to service and get data and attributes from tableName
        cur = self.con.cursor()

        # Test if the measuring point exists
        sql = """
        SELECT mp.obj_id
        FROM qgep_od.measuring_point mp
        JOIN qgep_od.wastewater_networkelement ne ON ne.fk_wastewater_structure = mp.fk_wastewater_structure
        WHERE ne.obj_id = '{reach_obj_id}'
        AND kind = '{MEASURING_POINT_KIND}'
        """.format(MEASURING_POINT_KIND=MEASURING_POINT_KIND, reach_obj_id=reach_obj_id)
    
        cur.execute(sql)
        res = cur.fetchone()

        if res is None:
            # Measuring point doesnt exists, must be created
            # 4594 = technical purpose [TO VALIDATE]
            sql = """
            INSERT INTO qgep_od.measuring_point
            (damming_device, identifier, kind, purpose, remark, fk_wastewater_structure)
            SELECT 5721, NULL, '{MEASURING_POINT_KIND}', 4594, '{NON_PHYSICAL_REM}', ne.fk_wastewater_structure 
            FROM qgep_od.wastewater_networkelement ne 
            WHERE ne.obj_id = '{reach_obj_id}'
            RETURNING obj_id
            """.format(MEASURING_POINT_KIND=MEASURING_POINT_KIND, NON_PHYSICAL_REM=NON_PHYSICAL_REM, reach_obj_id=reach_obj_id)
            try:
                cur.execute(sql)
            except psycopg2.ProgrammingError:
                self.feedback.reportError(str(psycopg2.ProgrammingError), True)
                return None
            res = cur.fetchone()
            mp_obj_id = res[0]
            self.con.commit()
            del cur
        else:
            mp_obj_id = res[0]
        return mp_obj_id

    def create_measurement_series(self, mp_obj_id, sim_description):

        """
        Creates a measurement serie or get its id.

        Parameters:
        mp_obj_id (string): measurement point object ID
        sim_description (string): description of the simulation

        Returns:
        mp_obj_id: measuring point object ID

        """

        # Connects to service
        cur = self.con.cursor()

        # Test if the measurement serie exists
        sql = """
        SELECT obj_id FROM qgep_od.measurement_series
        WHERE remark = '{sim_description}'
        AND fk_measuring_point = '{mp_obj_id}'
        """.format(sim_description=sim_description, mp_obj_id=mp_obj_id)
    
        cur.execute(sql)
        res = cur.fetchone()

        if res is None:
            # Measuring point doesnt exists, must be created
            # 3217 = other [TO VALIDATE]
            # No dimension, else we would need to create four measurements series l/s m/s m - [TO VALIDATE]
            sql = """
            INSERT INTO qgep_od.measurement_series
            (identifier, kind, remark, fk_measuring_point)
            VALUES
            (null, 3217, '{sim_description}', '{mp_obj_id}') 
            RETURNING obj_id
            """.format(sim_description=sim_description, mp_obj_id=mp_obj_id)

            try:
                cur.execute(sql)
            except psycopg2.ProgrammingError:
                self.feedback.reportError(str(psycopg2.ProgrammingError), True)
                return None
            ms_obj_id = cur.fetchone()[0]
            self.con.commit()
        else:
            ms_obj_id = res[0]
        del cur
        return ms_obj_id

    def create_measurement_result(self, ms_obj_id, measurement_type, measuring_duration, parameter, time, value):

        """
        Creates a measurement result or update it.

        Parameters:
        ms_obj_id (string): measurement serie object ID
        measurement_type (integer): type of measurement 5733=flow, 5734=level, 5732=other
        measuring_duration (integer): Time step of the simulation in seconds [TO VALIDATE]
        parameter (string): name of the SWMM parameter [TO VALIDATE]
        time (string): timestamp of the recorded result
        value (float): value of the measurement

        Returns:
        mr_obj_id: measurement result object ID

        """

        # Connects to service
        cur = self.con.cursor()

        # Test if the measurement result exists (same measurement serie, same time, same type)
        sql = """
        SELECT obj_id FROM qgep_od.measurement_result
        WHERE fk_measurement_series = '{ms_obj_id}'
        AND time = '{time}'
        AND remark = '{parameter}'
        AND measurement_type = {measurement_type}
        """.format(ms_obj_id=ms_obj_id, time=time, parameter=parameter, measurement_type=measurement_type)
    
        cur.execute(sql)
        res = cur.fetchone()

        if res is None:
            # Measurement result doesnt exists, must be created

            sql = """
            INSERT INTO qgep_od.measurement_result
            (identifier, measurement_type, measuring_duration, remark, time, value, fk_measurement_series)
            VALUES
            (null, {measurement_type}, {measuring_duration}, '{parameter}', '{time}', {value}, '{ms_obj_id}') 
            RETURNING obj_id
            """.format(measurement_type=measurement_type, measuring_duration=measuring_duration, parameter=parameter,
            time=time, value=value, ms_obj_id=ms_obj_id)

            try:
                cur.execute(sql)
            except psycopg2.ProgrammingError:
                self.feedback.reportError(str(psycopg2.ProgrammingError), True)
                return None
            mr_obj_id = cur.fetchone()[0]
            self.con.commit()
        else:
            mr_obj_id = res[0]
            # Measurement result exists, must be updated
            sql = """
            UPDATE qgep_od.measurement_result
            SET measuring_duration={measuring_duration}, value={value}
            WHERE obj_id = '{mr_obj_id}'
            RETURNING obj_id
            """.format(measuring_duration=measuring_duration,value=value,mr_obj_id=mr_obj_id)
            cur.execute(sql)
            mr_obj_id = cur.fetchone()[0]
            self.con.commit()
        del cur
        return mr_obj_id