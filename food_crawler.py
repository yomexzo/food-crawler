#Food_Crawler

import urllib2

def collect_data():

	#open a connection to a URL using urllib2
	webUrl = urllib2.urlopen("http://current.ischool.utoronto.ca/ischool")

	#get the result code and print it. 
	#ex: 200 OK, 404 not found
	print "Result Code: " + str(webUrl.getcode())

	#get the data from the URL and print it out.
	data = webUrl.read()
	print data

	# # webURL.feed(data)
	# f = data
	# if f.mode == "r":
	# 	contents = f.read()
	# 	parser.feed(contents)

if __name__ == "__main__":
	collect_data()