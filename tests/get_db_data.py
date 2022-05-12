import pyodbc

server = 'BAZILE88-PC\SQLEXPRESS'
database = 'SwagLabs'
query = 'SELECT username, userpassword, assertion FROM Users'

def get_query_data(server, database, query):
    db = pyodbc.connect('Driver={SQL Server};Server=%s;Database=%s;Trusted_Conection=yes;' % (server, database))
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

login_form_parameters = get_query_data(server, database, query)