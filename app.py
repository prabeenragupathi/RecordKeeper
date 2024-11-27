import db
import os
from tabulate import tabulate

os.system("cls") # to clear output screen

# ? now init the database
db_instance = db.initDB('prabeen')

#? creating table
table_name = 'bio'
table_structure = {
    'id': 'INT',
    'name': 'VARCHAR(30)',
    'salary': 'INT',
    'PRIMARY KEY(id)': ''
}

db.createTable(table_name, table_structure, db_instance)

def insertion() -> dict:
    id = input("Enter ID: ")
    name = input("Enter NAME: ")
    salary = input("Enter SALARY: ")
    
    return {'id': id, 'name': name, 'salary': salary}

def updation() -> dict:
    id = input("Enter ID: ")
    name = input("Enter New NAME: ")
    salary = input("Enter New SALARY: ")
    
    return {'id': id, 'name': name, 'salary': salary}

def deletion():
    id = input("Enter the Id: ")
    db.delete(table_name, id, db_instance)

def printRecord(id=None):
    try:
        '''
            # * it returns fetched data, colums name of the table
            # * header: columns names of the tables
            # * data: fetech record from DB
        '''
        result = None
        if id is None:
            result = db.getRecords(table_name, db_instance)
        else:
            result = db.getRecords(table_name, db_instance, id)
            
        print("------Bio Data Record------")
        if result is not None: 
            print(tabulate(result['data'], headers=result['header'], tablefmt='fancy_grid'))
    except Exception as error:
        print(error)

while(True):
    print('''
        1. Insert
        2. Update
        3. Delete
        4. List All
        5. Search
        6. Records Count
        0. Exit
        ''')
    choice = int(input("Enter you choice :> "))
    
    if choice == 0:
        db.closeDB(db_instance)
        exit(0)
        
    elif choice == 1:
        data = insertion()
        db.insert(table_name, data, db_instance)
        
    elif choice == 2:
        updatedData = updation()
        db.update(table_name, updatedData, db_instance)
        
    elif choice == 3:
        deletion()

    elif choice == 4:
        os.system('cls')
        printRecord()
    
    elif choice == 5:
        os.system('cls')
        id = input('Enter id to Search: ')
        printRecord(id)
    
    elif choice == 6:
        count = db.getRecordCount(table_name, db_instance)
        print(f'Total Records: {str(count[0])}')
    else:
        print("Invalid Input")