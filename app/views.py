from flask import render_template, flash, redirect, request
from app import app
from forms import SearchForm
import httplib
import re
from app import mysql
from search import searchWord


#used for adding img url into database
def LikeImage(smallURL, bigURL):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from liked where url_s = '"+smallURL+"'")
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT into liked values ('', '"+smallURL+"','"+bigURL+"')")
        conn.commit()
        cursor.close()
        print "INSERT"
        return "This image is liked!"
    else:
        cursor.close()
        print "already liked"
        return "This image has already been liked!"

#used for querying liked images from database
def reviewLiked():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from liked")
    data = cursor.fetchall()
    cursor.close()
    print "view"
    return [dict(small=row[1], big=row[2]) for row in data]

#used for removing disliked image
def dislikeImage(smallURL, bigURL):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE from liked where url_s = '"+smallURL+"'")
    conn.commit()
    print "delete"

@app.route('/flickr', methods = ['GET', 'POST'])
def search():
    form1 = SearchForm()
    m = []
    entries = {}
    message = None
    if form1.validate_on_submit():
    	keywords = form1.query.data
    	  #parse the HTTP response
        m = searchWord(keywords)

    elif request.form.get("like") != None:
        smallURL = request.form.get("small")
        bigURL = request.form.get("big")
        message = LikeImage(smallURL, bigURL)
        return message

    elif request.form.get("review") != None:
        entries = reviewLiked()
        
    elif request.form.get("dislike") != None:
        smallURL = request.form.get("small")
        bigURL = request.form.get("big")
        dislikeImage(smallURL, bigURL)
        entries = reviewLiked()
    return render_template('search.html',
        title = 'Flickr Search',
        form1 = form1,
        liked = entries,
        imgs = m,
        message = message)
    
