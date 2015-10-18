__author__ = 'Claude'

import MySQLdb


def execute_sql(sql_command):
    db = MySQLdb.connect("localhost", "root", "wuzher1||", "vms")
    cursor = db.cursor()
    try:
        cursor.execute(sql_command)
        db.commit()
        results = cursor.fetchall()
    except:
        db.rollback()
        results = "error"
    db.close()
    return results


if __name__ == '__main__':
    print(execute_sql("SELECT * FROM vm_user"))
