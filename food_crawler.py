#Food_Crawler

import urllib2
from HTMLParser import HTMLParser
from flask import Flask

base_url = 'http://current.ischool.utoronto.ca'
app = Flask(__name__)

all_events = []
current_event = {}
calendar_depth = 0
event_depth = 0
title_found = False
start_found = False
end_found = False
single_date_used = False

class CalendarParser(HTMLParser):
  # function to handle an opening tag in the doc
  # this will be called when the closing ">" of the tag is reached
  def handle_starttag(self, tag, attrs):
    global calendar_depth, current_event

    if calendar_depth == 3 and tag == 'a':
      calendar_depth = 4

    for name, value in attrs:
      if calendar_depth == 0 and name == 'class' and 'has-events' in value:
        calendar_depth = 1
        break
      elif calendar_depth == 1 and name == 'class' and 'view-item' in value:
        calendar_depth = 2
        break
      elif calendar_depth == 2 and name == 'class' and 'view-field' in value:
        calendar_depth = 3
        break
      elif calendar_depth == 4 and name == 'href':
        current_event['href'] = value
        break

  def handle_data(self, data):
    global calendar_depth, current_event, all_events

    if calendar_depth == 4:
      calendar_depth = 0
      current_event['title'] = data
      all_events.append(current_event)
      current_event = {} #reset

class EventParser(HTMLParser):

  def handle_starttag(self, tag, attrs):
    global title_found, event_depth, current_event, start_found, single_date_used, end_found

    for name, value in attrs:
      if name == 'class' and value == 'title':
        current_event['title'] = ''
        title_found = True
      if name == 'class' and value == 'date-display-start':
        start_found = True
        current_event['start'] = ''
      if name == 'class' and value == 'date-display-end':
        end_found = True
        current_event['end'] = ''
      if name == 'class' and value == 'date-display-single':
        single_date_used = True
        current_event['single_date'] = ''

  def handle_endtag(self, tag):
    global title_found, start_found, current_event, end_found

    if tag == 'h1' and title_found:
      title_found = False
    if tag == 'span' and start_found:
      start_found = False
    if tag == 'span' and end_found:
      end_found = False

  def handle_data(self, data):
    global title_found, current_event, start_found, single_date_used, end_found

    if title_found:
      current_event['title'] += data

    if start_found:
      if 'single_date' in current_event:
        current_event['start'] += current_event['single_date'] + data
      else:
        current_event['start'] += data

    if end_found:
      if 'single_date' in current_event:
        current_event['end'] += current_event['single_date'] + data
      else:
        current_event['end'] += data

    if single_date_used:
      current_event['single_date'] += data
      single_date_used = False


  def handle_entityref(self, data):
    global title_found, start_found, current_event

    if title_found:
      current_event['title'] += '&' + data + ';'


@app.route("/")
def main():
  global base_url, current_event

  response = '<!DOCTYPE html>'
  response += '<html>'
  response += '<head>'
  response += '</head>'
  response += '<body>'
  webUrl = urllib2.urlopen(base_url + "/calendar")
  data = webUrl.read()

  calendarParser = CalendarParser()
  calendarParser.feed(data)

  response += '<table border="1" cellpadding="5">'
  response += '<tr>'
  response += '<th>Title</th>'
  response += '<th>Duration</th>'
  response += '<th>HREF</th>'
  response += '</tr>'
  for event in all_events:
    current_event = event
    
    data = urllib2.urlopen(base_url + event['href']).read();
    eventParser = EventParser()
    eventParser.feed(data)
    
    event = current_event

    response += '<tr>'
    response += '<td>' + event['title'] + '</td>'
    response += '<td>' + event['start'] + ' to ' + event['end'] + '</td>'
    response += '<td><a target="_blank" href="' + base_url + event['href'] +'">' + event['href'] +'</a></td>'
    response += '</tr>'

  # .has-events .view-item .view-field a
  response += '<table>'
  response += '</body>'
  response += '</html>'

  return response

if __name__ == "__main__":
    app.run()
    # main()
