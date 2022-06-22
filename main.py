import os
import pyodbc 
from tqdm import tqdm


skip_identity_insert = [
    'ActivityLog',
    'GFWAnalyses',
    'GFWAnalyses-bu06072022',
    'GFWLists',
    'GFWLists-bu06082022',
    'Organizations',
    'analysis-administrativeAreas-bu06172022',
    'analysis-administrativeAreas-stg',
    'analysis-oilPalmConcessions-bu06082022'
    'analysis-oilPalmConcessions-stg',
    'analysis-oilPalmConcessions-bu06082022',
    'analysis-oilPalmConcessions-stg',
    'analysis-palmOilMills',
    'analysis-palmOilMills-bu06032022',
    'analysis-palmOilMills-stg',
    'analysis-protectedAreas-bu06172022',
    'analysis-protectedAreas-stg',
    'analysis-rspoOilPalmConcessions-bu06082022',
    'analysis-rspoOilPalmConcessions-stg',
    'geometry_columns',
    'list-administrativeAreas',
    'spatial_ref_sys',
    'temp_analysis_table'
]

not_convert = [
    'geometry_columns',
    'spatial_ref_sys',
    'temp_analysis_table'
]

def create_cnxn():
    cnxn = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                server='127.0.0.1,1433',
                database='gfwpro',
                uid='sa',
                pwd='R@@t123456',
                TrustServerCertificate='yes')
    return cnxn



def get_scripts(path):
    print(f"Reading files to process from directory: {path}")
    directory_files = os.listdir(path)
    directory_files = list(
        filter(
            lambda x: '.sql' in x,
            directory_files,
        )
    )
    directory_files.sort()
    return directory_files

def execute_scripts(script_path):
    cnxn = create_cnxn()
    with open(script_path) as sql_cmd:
        data = sql_cmd.read()
        data = data.replace("\ngo", "");
        data = data.replace("\n", "");
        cur = cnxn.cursor();
        cur.execute(data)
    cnxn.commit()
    cnxn.close();

def execute_scripts_procedure(script_path):
    cnxn = create_cnxn()
    with open(script_path) as sql_cmd:
        data = sql_cmd.read()
        data = data.replace("\t", " ");
        data = data.split('\ngo')

        for line in data:
            if line != '':
                line = line.replace("\n", " ")
                cur = cnxn.cursor();
                try:
                    cur.execute(line)
                except:
                    print(script_path)
                    continue
        cnxn.commit()
        cnxn.close();

def execute_scripts_line(script_path):
    cnxn = create_cnxn()
    table_name = script_path.replace("./data/gfwpro_dbo_", "").replace(".sql", "")
    if table_name not in not_convert:
        table_name = table_name.replace("_", "-")
    
    print(f'Table {table_name}')
    with open(script_path) as sql_cmd:
        cur = cnxn.cursor();
        if table_name not in skip_identity_insert:
            cur.execute(f"SET IDENTITY_INSERT  gfwpro.dbo.[{table_name}] ON;")
        lines = sql_cmd.readlines()
        for line in lines:
            if line != '':    
                try:
                    cur.execute(line)
                except:
                    continue
        if table_name not in skip_identity_insert:
            cur.execute(f"SET IDENTITY_INSERT  gfwpro.dbo.[{table_name}] OFF;")
    cnxn.commit()
    cnxn.close();

create_files = get_scripts('./create_table')
print("Found {} tables".format(len(create_files)))
for file in tqdm(create_files):
    execute_scripts('./create_table/' + file)
print("Create Table Done")

procedure_files = get_scripts('./procedure')
print("Found {} procedures".format(len(procedure_files)))
for file in tqdm(procedure_files):
    execute_scripts_procedure('./procedure/' + file)
print("Procedure Table Done")

data_files = get_scripts('./data')
print("Found {} files to insert data".format(len(data_files)))
for file in tqdm(data_files):
    execute_scripts_line('./data/' + file)
print("Insert Table Done")

# import pdb; pdb.set_trace()