from flask import Blueprint,current_app,request
import json

transactions=Blueprint('transactions',__name__)

@transactions.route('/getTransactions')
def getTransactions():
  return "<h3>Get transactions</h3>"

@transactions.route('/bookIssue',methods=['POST'])
def bookIssue():
  data=json.loads(request.data)
  mysql=current_app.config['mysql']
  cur=mysql.connection.cursor()
  
  cur.execute("""
    INSERT INTO transactions (member_id,book_id,issue_date,rent_per_day,is_returned)
    VALUES (%s,%s,%s,%s,'no')
  """,( int(data['selectedMember']),int(data['selectedBook']), data['issueDate'], int(data['rentPerDay']) ))
  
  cur.execute("""
    UPDATE books
    SET available_stock=available_stock-1
    WHERE id=%s
  """,( int(data['selectedBook']), ))

  mysql.connection.commit()
  cur.close()
  return json.dumps("ok")

@transactions.route('/bookReturn',methods=['POST'])
def bookReturn():
  data=json.loads(request.data)
  mysql=current_app.config['mysql']
  cur=mysql.connection.cursor()
  
  #update the transaction with return book data
  cur.execute("""
    UPDATE transactions
    SET is_returned='yes',return_date=%s,total_rent=%s,amount_paid=%s,new_outstanding_debt=%s
    WHERE id=%s
  """,( data['returnDate'],int(data['totalBookRent']), int(data['paymentAmount']), int(data['newOutstandingDebt']),int(data['txnId']) ))
  
  #increase the available stock
  cur.execute("""
    UPDATE books
    SET available_stock=available_stock+1
    WHERE id=%s
  """,( int(data['bookId']), ))

  #update the member's outstanding debt
  cur.execute("""
    UPDATE members
    SET debt=%s
    WHERE id=%s
  """,( int(data['newOutstandingDebt']), int(data['memberId']) ))

  mysql.connection.commit()
  cur.close()
  return json.dumps("ok")

@transactions.route('/getAllTransactions',methods=['GET'])
def getAllTransactions():
  mysql=current_app.config['mysql']
  cur=mysql.connection.cursor()
  cur.execute("""
    SELECT transactions.*, books.title, books.authors, members.name, members.email FROM transactions
    INNER JOIN books
    ON transactions.book_id=books.id
    INNER JOIN members
    ON transactions.member_id=members.id
  """)
  result=cur.fetchall()

  for txn in result:
    if txn['issue_date']:
      txn['issue_date']=txn['issue_date'].strftime('%Y-%m-%d') #format as needed
    if txn['return_date']:
      txn['return_date']=txn['return_date'].strftime('%Y-%m-%d')

  return json.dumps(result)