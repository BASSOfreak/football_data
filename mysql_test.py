import mysql.connector

cnx = mysql.connector.connect(user='root', password='MyNewPass',
                              host='127.0.0.1',
                              database='football_data')
							  
cursor = cnx.cursor()

statement = "INSERT INTO clubs (id, player_number, name) VALUES (12, 26, 'AS Roma')"
cursor.execute(statement)

cnx.commit()

cursor.close()


cnx.close()