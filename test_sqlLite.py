#import libraries, allows to connect to sqlLite dbs and to run SQL-queries etc
import sqlite3

#initialize connection to database
#sqlLite3stores all its connections/parameters in a file --> we are goin to create 'data.db' as this file (if not connected to database)
#sqllite is 'light' --> 3everything is saved in one file (see above), but is therefore also slower than others (e.g Postgrel etc)
#data.db will be created upon first run of this script and will contain ections taken (--> binary file)
connection = sqlite3.connect('data.db')

# acts like a cursor on a computer --> allows to select tjings or start somewhere
#e.g. can start selecting at beginning of database, run query, store results etc.
cursor = connection.cursor()

#SQL-query --> HERE: table creation
create_table = " CREATE TABLE users (id int, username text, password text)"

#run query --> using cursor
cursor.execute(create_table)

#create data to database ('users)
user = [
    (1, 'monkey', 'te amooo'),
    (2, 'lasuno', 'asdf'),
    (3, 'test1', 'asdf'),
    (4, 'blabla', 'mofo'),
    (5, 'testXXX', 'djthrsx')
]

#write query using placeholdres to insert data into database table (here: table to be inserted to is 'users')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

#retrieve data from data.db-file (or later on from database)
select_query = "SELECT * FROM users"

#run insert-query --> execute(insert_query_to_be_run, data_to_be_inserted)
# cursor.execute(insert_query, user)
#to run many queries --> e.g. insert many rows from a list use executemany() instead
cursor.executemany(insert_query, user)
#retrieve info and print out info per row:
for row in cursor.execute(select_query):
    print(row)


#tell connection to save changed (inserted data) to table/database and close connection
connection.commit()
connection.close()

