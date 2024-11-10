from flask import Blueprint,current_app,request
import json

members=Blueprint('members',__name__)

@members.route('/getMembers')
def getMembers():
    return "<h3>Get members</h3>"

@members.route('/addNewMember',methods=['POST'])
def addNewMember():
    data=json.loads(request.data)
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    try:
        cur.execute("""
            INSERT INTO members (name,age,email,debt)
            VALUES (%s,%s,%s,%s)
        """,( data['name'],int(data['age']),data['email'],int(data['debt']) ))
        mysql.connection.commit()
    except Exception as e:
        print("error -",e);
        return (json.dumps(f"Error - {e}"),500)
    cur.close()
    return json.dumps("Member added")

@members.route('/getCurrentMembers',methods=['GET'])
def getCurrentMembers():
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM members
    """)
    result=cur.fetchall()
    cur.close()
    return json.dumps(result)

@members.route('/editMember',methods=['POST'])
def editMember():
    data=json.loads(request.data)
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        UPDATE members
        SET name = %s, age=%s, debt=%s
        WHERE id=%s
    """,(data['name'], int(data['age']), int(data['debt']),data['id']))
    mysql.connection.commit()
    cur.close()
    return json.dumps("ok")

@members.route('/deleteMember',methods=['POST'])
def deleteMember():
    data=json.loads(request.data)
    memberId=int(data['memberId'])
    
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        DELETE FROM members
        WHERE id=%s
    """,(memberId,))
    mysql.connection.commit()
    cur.close()
    return json.dumps("ok")