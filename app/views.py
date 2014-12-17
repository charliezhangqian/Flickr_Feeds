from flask import render_template, flash, redirect
from app import app
from forms import SearchForm
import httplib
import re

@app.route('/flickr', methods = ['GET', 'POST'])
def search():
    form = SearchForm()
    m = []
    if form.validate_on_submit():
    	keywords = form.query.data
    	p = re.compile("\s")
    	keywords = p.sub("",keywords) #remove the spaces in keywords
    	conn = httplib.HTTPConnection("www.flickr.com")
    	url = "http://api.flickr.com/services/feeds/photos_public.gne?tags="+keywords;
    	conn.request("GET", url)  #send Http GET request to flickr web feeds
    	response = conn.getresponse()
        data = response.read();
        p = re.compile("img src.*?(http.*?\.jpg).*?enclosure.*?(http.*?\.jpg)", re.S)  #parse the HTTP response
        m = p.findall(data)
    return render_template('search.html',
        title = 'Flickr Search',
        form = form,
        imgs = m)
