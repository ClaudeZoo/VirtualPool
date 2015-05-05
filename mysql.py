__author__ = 'Claude'

import MySQLdb


db = MySQLdb.connect("localhost", "vm_manager", "thss&2014", "vms")
cursor = db.cursor()
sql_command = "test"
cursor.execute(sql_command)
results = cursor.fetchall()
for row in results:
    id = row[0]
    name = row[1]

db.close()