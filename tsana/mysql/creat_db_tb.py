import mysql.connector

cnx = mysql.connector.connect(user='zy', password='111282',
                              host='127.0.0.1')
cursor = cnx.cursor()

cursor.execute('''
CREATE DATABASE IF NOT EXISTS db_time_series;
''')

cursor.execute('USE db_time_series;')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_time_series
(
site CHAR(4),
cmpt CHAR(1),
t DATETIME,
y DOUBLE,
ysd DOUBLE,
PRIMARY KEY (site, cmpt, t)
);
''')

cnx.commit()

cnx.close()
