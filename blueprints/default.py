from flask import Blueprint,current_app
import json

default=Blueprint('default',__name__)

@default.route('/test_default')
def test_default():
    print("Default blueprint")
    return "<h3>Default blueprint</h3>"


# @default.route('/myfunc')
# def myfunc():
#     mysql=current_app.config['mysql']
#     cur=mysql.connection.cursor()
#     try:
#         cur.execute("""
#             SELECT CONSTRAINT_NAME
#             FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
#             WHERE TABLE_NAME = 'transactions' AND COLUMN_NAME = 'book_id';
#         """)
#         result=cur.fetchall()
#         return json.dumps(result)
#         mysql.connection.commit()
#     except Exception as e:
#         print("Error - ",e)
#         return(f"Error - {e}")
#
#     cur.close()
#     return "ok"
#
# @default.route('/myfunc2')
# def myfunc2():
#     mysql=current_app.config['mysql']
#     cur=mysql.connection.cursor()
#     try:
#         cur.execute("""
#             ALTER TABLE transactions
#             ADD FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE;
#         """)
#         mysql.connection.commit()
#     except Exception as e:
#         print("Error - ",e)
#         return(f"Error - {e}")
#
#     cur.close()
#     return "ok"