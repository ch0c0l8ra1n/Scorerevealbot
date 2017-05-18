import json
import urllib.request
from http.cookiejar import CookieJar
import time

alreadydone = []

def comment(newitem):
	#Checking if its a top level comment or not
	#for top level
	newcomment = "null"
	if item["data"]["parent_id"][:2] == "t1":
		newlink= newitem["data"]["link_permalink"]+newitem["data"]["parent_id"][3:]+"/.json?limit=1"
		newstuff=urllib.request.urlopen(newlink).read()
		nsparsed = json.loads(newstuff.decode())
		score = nsparsed[1]["data"]["children"][0]["data"]["score"]
		up = nsparsed[1]["data"]["children"][0]["data"]["ups"]
		down = nsparsed[1]["data"]["children"][0]["data"]["downs"]
		newcomment = 'Your parent comment has a score of {}.\n\nUpvotes = {}\n\nDownvotes = {}'.format(score,up,down)
    	payload = {
    		"thing_id":item["data"]["name"],
    		"text":newcomment,
    		"id":"commentreply_"+item["data"]["name"],
    		"r":item["data"]["subreddit"],
    		"uh":uhash,
    		"renderstyle":"html"
    	}
    	data = urllib.parse.urlencode(payload)
    	binary_data = data.encode('UTF-8')
    	req = urllib.request.Request("https://www.reddit.com/api/comment", binary_data)
    	resp = urllib.request.urlopen(req)
    	alreadydone.append(item["data"]["name"])
#Enter username and password here
user = ""
passwad = ""

usagent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"

cj = CookieJar()
opener= urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent',usagent)]
urllib.request.install_opener(opener)
authentication_url = 'https://ssl.reddit.com/post/login'
payload = {
	'op':'username',
	'user': user,
	'passwd': passwad
}

data = urllib.parse.urlencode(payload)
binary_data = data.encode('UTF-8')
req = urllib.request.Request(authentication_url, binary_data)
resp = urllib.request.urlopen(req)
url = "https://www.reddit.com/api/me.json"
response = urllib.request.urlopen(url)
your_json = response.read()
parsed = json.loads(your_json.decode())
uhash= (parsed["data"]["modhash"])
print ("logged in")
i=1
while True:
	time.sleep(1)
	url = "https://www.reddit.com/r/all/comments/.json?limit=100"
	req = urllib.request.Request(url,None)
	response=urllib.request.urlopen(req)
	your_json = response.read()
	parsed = json.loads(your_json.decode())
	items = parsed["data"]["children"]
	for item in items:
		if item["data"]["body"] == "scorereveal" and item["data"]["name"] not in alreadydone:
			comment(item)

