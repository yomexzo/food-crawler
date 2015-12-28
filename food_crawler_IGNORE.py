#Food_Crawler_2

# import module to handle data retrieval from web url.
import urllib2
# import module to handle parsing of html files.
from HTMLParser import HTMLParser
#import module to handle file writing functions.
import sys


f = open('test.txt', 'w')
sys.stdout = f
# print all_events

# identify the base url from which you gather your data. 
base_url = 'http://current.ischool.utoronto.ca/calendar'



# create an empty dictionary to store all events.
all_events = {}
# create an empty dictionary to store current event being working on.
current_event = []

#set a base depth from which to track nested levels in html code.
calendar_depth = 0


# define a class to handle parsing of html file.
# import HTMLParser methods from the HTMLParser module for use.
class CalendarParser(HTMLParser):
	# function to handle an opening tag in the html document.
	# this will be called when the closing '>' of the tag is reached.
	def handle_starttag(self, tag, attrs):
		# make the base depth variable and the empty current event dictionary available to this function.
		global calendar_depth, current_event

		if calendar_depth == 3 and tag == 'a':
			calendar_depth = 4

		# start a for loop which looks inside the HTML file for the name (key), and value of attributes.
		for name, value in attrs:
			# loop goes down level by level until it reaches the 'href' with the value (url) we are looking for. 
			if calendar_depth == 0 and name == "class" and "has-events" in value:
				calendar_depth = 1
				break
			elif calendar_depth == 1 and name == "class" and "has-events" in value:
				calendar_depth = 2
				break
			elif calendar_depth == 2 and name == "class" and "has-events" in value:
				calendar_depth = 3
				break
			elif calendar_depth == 3 and name == "class" and "has-events" in value:
				break
			elif calendar_depth == 4 and name == "class" and "has-events" in value:
				current_event['href'] = value
				break

	# function to handle the data in between the tags.
	def handle_data(self, data):
		# make the depth level, and the current event and all events dictionaries available to this function.
		global calendar_depth, current_event, all_events

		if calendar_depth == 4:
			calendar_depth = 0
			current_event['title'] = data
			all_events.append(current_event)
			current_event = []


def main():
	global base_url, current_event

	webUrl = urllib2.urlopen(base_url)
	data = webUrl.read()

	calendarParser = CalendarParser()
	calendarParser.feed(data)

	print calendarParser


if __name__ == "__main__":
    main()
