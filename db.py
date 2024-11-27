import mysql.connector
from dotenv import load_dotenv
import os

# ? connection & cursor varibales
conn = None
cur = None

# * environment variables import
load_dotenv() #this methods loads the .env file

#get those credentials from env
credentials = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PWD')
}

def initDB(databaseName:str):
    try:
        conn = mysql.connector.connect(**credentials)
        conn.database = databaseName
        # ? creating cursor object
        cur = conn.cursor()
        
        return {'conn': conn,
                'cur': cur
        }
    except Exception as error:
        print(f'Error: {error}')

def closeDB(db:dict):
    if db['conn'] is not None:
        db['conn'].close()
    
    if db['cur'] is not None:
        db['cur'].close()

def createTable(tableName:str, colums:dict, db:dict):
    table_define = ', '.join([f"{name} {dType}" for name, dType in colums.items()])
    table_qry = f'''
        CREATE TABLE IF NOT EXISTS {tableName}(
            {table_define}
        )
    '''
    
    try:
        db['cur'].execute(table_qry)
        db['conn'].commit()
        
    except Exception as error:
        print(f'Error: {error}')

def insert(table:str, data:dict, db:dict):
    columns = ', '.join(data.keys())
    placeholder = ', '.join(['%s'] * len(data.keys()))
    values = tuple(data.values())
    
    insert_qry = f'''
        INSERT INTO {table} ({columns}) VALUES ({placeholder})
    '''
    try:
        db['cur'].execute(insert_qry, values)
        db['conn'].commit()
        print("Inserted successfully...")
        
    except Exception as error:
        print(f'Insertion Error: {error}')

def update(table:str, data:dict, db:dict):
    #checking whethear the data has id to update
    if 'id' not in data:
        print("Id is required to update")
        return
    
    id = data.pop('id') #returns the id value & removed that key-value from that data dictnary
    
    set_clause = ', '.join([f'{key} = %s' for key in data.keys()])
    values = tuple(data.values())
    
    update_qry = f'''
        UPDATE {table} SET {set_clause} WHERE id = {id}
    '''
    
    try:
        db['cur'].execute(update_qry, values)
        db['conn'].commit()
        print('Updated Successfully...')
        
    except Exception as error:
        print(f'Update Error: {error}')

def getRecords(table:str, db:dict, id:str=None):
    if id is not None: #fetch one specific data
        fetch_qry = f'''
            SELECT * FROM {table} WHERE id = %s
        '''
        result = None
        try:
            check_qry = f'''
                SELECT 1 FROM {table} WHERE id = %s
            '''
            db['cur'].execute(check_qry, (id,))
            exists = db['cur'].fetchone()
            
            if exists:
                db['cur'].execute(fetch_qry, (id,))
                result = {'data': db['cur'].fetchall()}
                #getting column names of the table
                column_name = [desc[0] for desc in db['cur'].description]
                result.update({'header': column_name})
            else:
                print(f'No record Found with ID: {id}')
            
        except Exception as error:
            print(f'Fetching Error: {error}')
        
        return result
    
    fetch_qry = f'''
            SELECT * FROM {table}
        '''
    result = None
    try:
        #fetch all data
        db['cur'].execute(fetch_qry)
        result = {'data': db['cur'].fetchall()}
        #getting column names of the table
        column_name = [desc[0] for desc in db['cur'].description]
        result.update({'header': column_name})
    except Exception as error:
        print(f'Fetching Error: {error}')
    
    return result

def delete(table:str, id:str | int, db:dict):
    delete_qry = f'''
        DELETE FROM {table} WHERE id = %s
    '''
    # ! before deleting check whether is exists on table
    check_qry = f'''
        SELECT 1 FROM {table} WHERE id = %s
    '''
    try:
        db['cur'].execute(check_qry, (id,))
        exists = db['cur'].fetchone()
        
        if exists:
            db['cur'].execute(delete_qry, (id,))
            db['conn'].commit()
            print("Deleted Successfully...")
        else:
            print(f'No Record found with ID: {id}')
    except Exception as e:
        print(f'Deletion Error: {e}')

def getRecordCount(table:str, db:dict):
    count_qry = f'''
        SELECT COUNT(*) FROM {table}
    '''
    result = None
    try:
        db['cur'].execute(count_qry)
        result = db['cur'].fetchone()
    except Exception as e:
        print(e)
        
    return result
