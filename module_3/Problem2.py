import sqlite3
import argparse 

def get_tables_from_db(db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'") #to fetch all tables
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    connection.close()
    return tables
def get_table_info(db, table):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(f'PRAGMA table_info({table})') #to fetch all columns
    columns = cursor.fetchall()
    columns = [column[1] for column in columns]
    return columns
def execute_query(query_desc, query_file, db):
    print(query_desc)
    print(' ')
    with open(query_file, 'r') as file:
        query = file.read()
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    for answer in output:
        print(answer[0])
    print('\n')
    connection.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query_desc", type = str, help="Description of the query")
    parser.add_argument("--query_file", type = str, help="Query to be executed")
    parser.add_argument("--db", type = str, help="Database name")

    args = parser.parse_args()

    execute_query(args.query_desc, args.query_file, args.db)

if __name__ == "__main__":
    main()



