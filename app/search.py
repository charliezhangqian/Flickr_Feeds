import httplib
import re

def searchWord(keywords):
    p = re.compile("\s")
    keywords = p.sub("",keywords) #remove the spaces in keywords
    conn = httplib.HTTPConnection("www.flickr.com")
    url = "http://api.flickr.com/services/feeds/photos_public.gne?tags="+keywords;
    conn.request("GET", url)  #send Http GET request to flickr web feeds
    response = conn.getresponse()
    data = response.read();
    p = re.compile("img src.*?(http.*?\.jpg).*?enclosure.*?(http.*?\.jpg)", re.S)
    return p.findall(data)