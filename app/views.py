from flask import render_template, flash, redirect, request
from app import app
from forms import SearchForm
import httplib
import re
from app import mysql

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
        return "This image is liked"
    else:
        cursor.close()
        print "already liked"
        return "This image has already been liked"

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
    	p = re.compile("\s")
    	keywords = p.sub("",keywords) #remove the spaces in keywords
    	conn = httplib.HTTPConnection("www.flickr.com")
    	url = "http://api.flickr.com/services/feeds/photos_public.gne?tags="+keywords;
    	conn.request("GET", url)  #send Http GET request to flickr web feeds
    	response = conn.getresponse()
        data = response.read();
        p = re.compile("img src.*?(http.*?\.jpg).*?enclosure.*?(http.*?\.jpg)", re.S)  #parse the HTTP response
        m = p.findall(data)

    elif request.form.get("like") != None:
        smallURL = request.form.get("small")
        bigURL = request.form.get("big")
        message = LikeImage(smallURL, bigURL)

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
    
