from flask import render_template, flash, redirect
from app import app
from forms import LoginForm
import httplib
import re

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    m = []
    if form.validate_on_submit():
    	keywords = form.query.data
    	p = re.compile("\s")
    	keywords = p.sub("",keywords)
    	conn = httplib.HTTPConnection("www.flickr.com")
    	url = "http://api.flickr.com/services/feeds/photos_public.gne?tags="+keywords;
    	conn.request("GET", url)
    	response = conn.getresponse()
        data = response.read();
        p = re.compile("img src.*?(http.*?\.jpg).*?enclosure.*?(http.*?\.jpg)", re.S)
        m = p.findall(data)
    return render_template('search.html',
        title = 'Flickr Search',
        form = form,
        imgs = m)