from flask import Blueprint,request,current_app,jsonify
from datetime import datetime
import json
import requests

books=Blueprint('books',__name__)

@books.route('/getBooks')
def getBooks():
    return "<h3>Get books</h3>"

@books.route('/fetchNewBooks',methods=['POST'])
def fetchNewBooks():
    data=json.loads(request.data)
    booksRemaining=int(data['numBooks'])
    booksList=[]
    url='https://frappe.io/api/method/frappe-library'
    pageNum=0
    while booksRemaining>0:
        pageNum+=1
        params={
            'title':data['title'],
            'authors':data['author'],
            'page':pageNum
        }
        res=requests.get(url,params).json()
        resBooks=res['message']

        if not resBooks:
            break

        if(booksRemaining-len(resBooks) >= 0):
            booksList.extend(resBooks)
            booksRemaining-=len(resBooks)
        else:
            booksList.extend(resBooks[0:booksRemaining])
            booksRemaining=0

    return json.dumps(booksList)

@books.route('/addBooks',methods=['POST'])
def addBooks():
    mysql=current_app.config['mysql']
    books=json.loads(request.data)
    try:
        cur=mysql.connection.cursor()
        for book in books:
            cur.execute("""
                INSERT IGNORE INTO books(id,title,authors,average_rating,isbn,isbn13,language_code,num_pages,ratings_count,text_reviews_count,publication_date,publisher,available_stock)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,(int(book['bookID']),book['title'],book['authors'],book['average_rating'],book['isbn'],book['isbn13'],book['language_code'],book['  num_pages'],book['ratings_count'],book['text_reviews_count'],book['publication_date'],book['publisher'],book['available_stock']))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print('Error - ',e)
        return (f"Error - {e}",500)
    
    return json.dumps("ok");

@books.route('/getCurrentBooks',methods=['GET'])
def getCurrentBooks():
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM books
    """)
    result=cur.fetchall()
    cur.close()
    return json.dumps(result)

@books.route('/getAvailableBooks',methods=['GET'])
def getAvailableBooks():
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM books
        WHERE available_stock>0
    """)
    result=cur.fetchall()
    cur.close()
    return json.dumps(result)

@books.route('/getReturnableBooks',methods=['POST'])
def getReturnableBooks():
    data=json.loads(request.data)
    memberId=data['memberId']
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM transactions
        INNER JOIN books
        ON transactions.book_id=books.id
        INNER JOIN members
        ON transactions.member_id=members.id
        WHERE member_id=%s AND is_returned='no'
    """,(int(memberId),))
    result=cur.fetchall()
    for issueInfo in result:
        if issueInfo['issue_date']:
            issueInfo['issue_date']=issueInfo['issue_date'].strftime('%Y-%m-%d') #format as needed
    cur.close()
    return json.dumps(result)

@books.route('/stockEdit',methods=['POST'])
def stockEdit():
    data=json.loads(request.data)
    bookId=int(data['bookId'])
    newStock=int(data['newStock'])
    
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        UPDATE books
        SET available_stock = %s
        WHERE id=%s
    """,(newStock,bookId))
    mysql.connection.commit()
    cur.close()
    return json.dumps("ok")

@books.route('/deleteBook',methods=['POST'])
def deleteBook():
    data=json.loads(request.data)
    bookId=int(data['bookId'])
    
    mysql=current_app.config['mysql']
    cur=mysql.connection.cursor()
    cur.execute("""
        DELETE FROM books
        WHERE id=%s
    """,(bookId,))
    mysql.connection.commit()
    cur.close()
    return json.dumps("ok")
