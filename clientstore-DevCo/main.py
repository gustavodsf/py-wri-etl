import os
import pyodbc 
from tqdm import tqdm


skip_identity_insert = [
]

not_convert = [
]

def create_cnxn():
    cnxn = pyodbc.connect(driver='{ODBC Driver 18 for SQL Server}',
                server='127.0.0.1,1433',
                database='clientstore-DevCo',
                uid='GFWProUser',
                pwd='measure2010!',
                TrustServerCertificate='yes')
    return cnxn



def get_scripts(path, reverse = False):
    print(f"Reading files to process from directory: {path}")
    directory_files = os.listdir(path)
    directory_files = list(
        filter(
            lambda x: '.sql' in x,
            directory_files,
        )
    )
    directory_files.sort(reverse=reverse)
    return directory_files

def execute_scripts(script_path):
    cnxn = create_cnxn()
    cur = cnxn.cursor();
    print(script_path)
    with open(script_path) as sql_cmd:
        data = sql_cmd.read()
        data = data.replace("\ngo", "");
        data = data.replace("\n", "");
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
    with open(script_path) as sql_cmd:
        cur = cnxn.cursor();
        lines = sql_cmd.readlines()
        for line in lines:
            if line != '':    
                try:
                    cur.execute(line)
                except:
                    continue
    cnxn.close();

#create_files = get_scripts('./create_table', reverse=True)
#print("Found {} tables".format(len(create_files)))
#for file in tqdm(create_files):
#    print(file)
#    execute_scripts('./create_table/' + file)
#print("Create Table Done")

procedure_files = get_scripts('./procedure')
print("Found {} procedures".format(len(procedure_files)))
for file in tqdm(procedure_files):
    execute_scripts_procedure('./procedure/' + file)
print("Procedure Table Done")

#data_files = get_scripts('./data')
#print("Found {} files to insert data".format(len(data_files)))
#for file in tqdm(data_files):
#    execute_scripts_line('./data/' + file)
#print("Insert Table Done")

# import pdb; pdb.set_trace()