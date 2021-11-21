import psycopg2 as pgad
try:
    conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
    cur = conn.cursor()
    #print('PostgreSQL database version:')
    #cur.execute('SELECT * FROM \"fileSystem\".\"encryptionKeys\"')
    #cur.execute('SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name = \'encryptionKeys\';')
    #cur.execute('INSERT INTO \"fileSystem\".\"encryptionKeys\"(fileName,encrypt_key) VALUES(abc,def)')
    cur.execute('INSERT INTO \"public\".\"testTable\" VALUES(\'C::\',\'gif\')')
    #cur.execute('INSERT INTO testTable(fileName) VALUES(abc)')
        # display the PostgreSQL database server version
    #db_version = cur.fetchone()
    #print(db_version)
    conn.commit()
	# close the communication with the PostgreSQL
    cur.close()
except (Exception, pgad.DatabaseError) as error:
        print(error)
finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')


"""
User    Password  Group{Non-admin|Admin}
jeff              Non-admin
Shakeel           Admin 



"""

"""
fileName    encrypt_key     user_name   delete?


"""


"""
Delete:
Superuser - Admin - can delete public file/
Normal - Non-admin
Private files - private user can delete only.
Public file - Superuser(any),private user can delete.

View:
Public/Private

Write:
Public/Private

Read:
Public 
Private - private user can only.


"""


"""
Username    fileName    Access


Delete file - Delete Query -- COMPLETED
Permissions 
-- Table creation -- COMPLETED
-- Public/Private toggle
-- List files visibility
-- Delete button visibility 
-- Home button
-- Back button

Password Jacking Attack - Shakeel

"""
