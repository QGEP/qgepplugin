# -*- coding: utf-8 -*-

import psycopg2
import codecs

class QgepSwmm:
    
    def __init__(self, title, service, inpfile, inptemplate, outfile):
        self.title = title
        self.service = service
        self.input_file = inpfile
        self.options_template_file = inptemplate
        self.output_file = outfile

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
        except:
            print ('Table %s doesnt exists' %tableName)
            return None, None
        data = cur.fetchall()
        attributes = [desc[0] for desc in cur.description]
        
        return data, attributes
    
    
    def swmm_table(self, tableName):
        """ 
        Create swmm table
        
        Parameters:
        tableName (string): Name of the swmm section
    
        Returns:
        String: table content
        
        """
        
        # Create commented line which contains the field names
        fields = ""
        data, attributes = self.get_swmm_table(tableName)
        if data != None:
            for i,field in enumerate(attributes):
                # Does not write values stored in columns descriptions, tags and geom
                if field not in ('description', 'tag', 'geom'):
                    fields+=field +"\t"
            
            # Create input paragraph
            tbl =u'['+tableName+']\n'\
                ';;'+fields+'\n'
            for feature in data:
                for i, v in enumerate(feature):
                    # Write description
                    if attributes[i] == 'description' and str(v) != 'None':
                        tbl += ';'
                        tbl += str(v)
                        tbl += '\n'

                for i, v in enumerate(feature):
                    # Does not write values stored in columns descriptions, tags and geom
                    if attributes[i] not in ('description', 'tag', 'geom'):
                        if str(v) != 'None':
                            tbl += str(v)+'\t'
                        else: 
                            tbl += '\t'
                tbl += '\n'
            tbl += '\n'
            return tbl;
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
        options_template = open(self.options_template_file,'r').read()
        # Find and extract options
        indexStart = options_template.find('[%s]' %parameter_name)
        if indexStart == -1:
            # The balise options is not found
            print ('There is no [%s] in the template file' %parameter_name)
            return ''
        else:
            # Search for the next opening bracket
            indexStop = options_template[indexStart+1:].find('[')
            if indexStop == -1:
                # Copies text until the end of the file
                indexStop = len(options_template)
                optionText = options_template[indexStart:indexStop]+'\n\n'
            else:
                indexStop = indexStart+1+indexStop  
                optionText = options_template[indexStart:indexStop]
            return optionText
                
        
    def write_input(self):
        
        """ 
        Write the swmm input file
        
        """
    
        # From qgis swmm
        filename = self.input_file
        
        with codecs.open(filename, 'w',encoding='utf-8') as f:
                
            #Title / Notes
            #--------------
            f.write('[TITLE]\n')
            f.write(self.title+'\n\n')
            
            # Options
            #--------
            f.write(self.copy_parameters_from_template('OPTIONS'))
            f.write(self.copy_parameters_from_template('REPORT'))
            f.write(self.copy_parameters_from_template('FILES'))
            f.write(self.copy_parameters_from_template('EVENTS'))
            
            # Climatology
            #------------
            f.write(self.copy_parameters_from_template('HYDROGRAPHS'))
            f.write(self.copy_parameters_from_template('EVAPORATION'))
            f.write(self.copy_parameters_from_template('TEMPERATURE'))
           
            # Hydrology
            #----------
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
            #------------------
            f.write(self.swmm_table('JUNCTIONS'))
            # Create default junction to avoid errors
            f.write('default_qgep_node\t0\t0\n\n')
            f.write(self.swmm_table('OUTFALLS'))
            f.write(self.swmm_table('STORAGE'))
            f.write(self.swmm_table('COORDINATES'))
            
            f.write(self.copy_parameters_from_template('DIVIDERS'))
            
            # Hydraulics: links
            #------------------
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
            #--------
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
            #-------
            f.write(self.copy_parameters_from_template('CURVES'))
            
            # Time series
            #------------
            f.write(self.copy_parameters_from_template('TIMESERIES'))
            
            # Time patterns
            #--------------
            f.write(self.copy_parameters_from_template('PATTERNS'))
            
            # Map labels
            #-----------
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
        
        o = codecs.open(self.output_file,'r',encoding='utf-8')
        line = o.readline()
        noLine = 0
        lines=[]
        titleFound=False
        endTableFound = False
        while line:
            line = line.rstrip()
            # Search for the table title
            if line.find(table_title) != -1:
                titleFound = True
                lineAfterTitle = 0
            
            if titleFound and lineAfterTitle > 7 and line == '':
                endTableFound = True
            
            if titleFound and endTableFound == False and lineAfterTitle > 7:
                lines.append(line.split())
                
                
            if titleFound:       
                lineAfterTitle += 1
                
            noLine+=1
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
            curRes = {}
            curRes['id'] = d[0]
            curRes['type'] = d[1]
            curRes['average_depth'] = d[2]
            curRes['maximum_depth'] = d[3]
            curRes['maximum_hgl'] = d[4]
            curRes['time_max_day'] = d[5]
            curRes['time_max_time'] = d[6]
            curRes['reported_max_depth'] = d[7]
            result.append(curRes)
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
            
            curRes = {}
            curRes['id'] = d[0]
            curRes['type'] = d[1]
            curRes['maximum_flow'] = d[2]
            curRes['time_max_day'] = d[3]
            curRes['time_max_time'] = d[4]
            if d[1] == 'CONDUIT':
                curRes['maximum_velocity'] = d[5]
                curRes['max_over_full_flow'] = d[6]
                curRes['max_over_full_depth'] = d[7]
            elif d[1] == 'PUMP':
                curRes['max_over_full_flow'] = d[5]
                curRes['maximum_velocity'] = None
                curRes['max_over_full_depth'] = None
                
                
            result.append(curRes)
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
            
            curRes = {}
            curRes['id'] = d[0]
            curRes['shape'] = d[1]
            curRes['full_depth'] = d[2]
            curRes['full_area'] = d[3]
            curRes['hyd_rad'] = d[4]
            curRes['max_width'] = d[5]
            curRes['no_of_barrels'] = d[6]
            curRes['full_flow'] = d[7]
              
            result.append(curRes)
        return result
    
#    def save_node_depth_summary(self):
#        # Delete existing results
#        self.delete_table('nodes_results')
#        # Extract node depth table
#        data = self.extract_node_depth_summary()
#        con = None
#        sql = """
#        INSERT INTO qgep_swmm.nodes_results VALUES (
#        %(id)s, %(type)s, %(average_depth)s,
#        %(maximum_depth)s, %(maximum_HGL)s, %(time_max_day)s, 
#        %(time_max_time)s, %(reported_max_depth)s)
#        """
#        try:
#            con = psycopg2.connect(service=self.service)
#            cur = con.cursor()
#            cur.executemany(sql, data)
#            con.commit()
#        except (Exception, psycopg2.DatabaseError) as error:
#            print (error)
#
#        finally:
#            if con is not None:
#                con.close()
#        return
#    
#    def save_link_flow_summary(self):
#        # Delete existing results
#        self.delete_table('links_results')
#        # Extract node depth table
#        data = self.extract_link_flow_summary()
#        print (data)
#        con = None
#        sql = """
#        INSERT INTO qgep_swmm.links_results VALUES (
#        %(id)s, %(type)s, %(maximum_flow)s,
#        %(time_max_day)s, %(time_max_time)s,
#        %(maximum_velocity)s, %(max_over_full_flow)s,  %(max_over_full_depth)s)
#        """
#        try:
#            con = psycopg2.connect(service=self.service)
#            cur = con.cursor()
#            cur.executemany(sql, data)
#            con.commit()
#        except (Exception, psycopg2.DatabaseError) as error:
#            print (error)
#
#        finally:
#            if con is not None:
#                con.close()
#        return
#    
#    def save_cross_section_summary(self):
#        """Save the cross section summary output from the SWMM process"""
#                # Delete existing results
#        self.delete_table('xsections_results')
#        # Extract node depth table
#        data = self.extract_cross_section_summary()
#        con = None
#        sql = """
#        INSERT INTO qgep_swmm.xsections_results VALUES (
#        %(id)s, %(shape)s, %(full_depth)s,
#        %(full_area)s, %(hyd_rad)s, %(max_width)s, 
#        %(no_of_barrels)s, %(full_flow)s)
#        """
#        try:
#            con = psycopg2.connect(service=self.service)
#            cur = con.cursor()
#            cur.executemany(sql, data)
#            con.commit()
#        except (Exception, psycopg2.DatabaseError) as error:
#            print (error)
#
#        finally:
#            if con is not None:
#                con.close()
#        return
#    
#    def delete_table(self, table_name):
#        conn = None
#        rows_deleted = 0
#        try:
#            # connect to the PostgreSQL database
#            conn = psycopg2.connect(service=self.service)
#            # create a new cursor
#            cur = conn.cursor()
#            # execute the UPDATE  statement
#            cur.execute("DELETE FROM qgep_swmm.%s" %table_name)
#            # get the number of updated rows
#            rows_deleted = cur.rowcount
#            # Commit the changes to the database
#            conn.commit()
#            # Close communication with the PostgreSQL database
#            cur.close()
#        except (Exception, psycopg2.DatabaseError) as error:
#            print(error)
#        finally:
#            if conn is not None:
#                conn.close()
#        return rows_deleted
        

#PATH2SCHEMA = 'S:/2_INTERNE_SION/0_COLLABORATEURS/PRODUIT_Timothee/02_work/qgep_swmm/scripts/install_swmm_views.bat'
#TITLE = 'title simulation'
#PGSERVICE = 'pg_qgep_demo_data'
#INPFILE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\input\\qgep_swmm.inp'
#INPTEMPLATE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\simulation_parameters\\default_qgep_swmm_parameters.inp'
#OUTFILE = 'S:\\2_INTERNE_SION\\0_COLLABORATEURS\\PRODUIT_Timothee\\02_work\\qgep_swmm\\output\\swmm.out'

#subprocess.call([PATH2SCHEMA])   
#qs = qgep_swmm(TITLE, PGSERVICE, INPFILE, INPTEMPLATE, OUTFILE)
#qs.write_input()
#print ('done')
#qs.save_node_depth_summary()
#qs.save_link_flow_summary()
#qs.save_cross_section_summary()