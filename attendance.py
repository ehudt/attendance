#!/usr/bin/python
# -*- coding: utf-8 -*-

# Scrape Knesset website and retrieve live member attendance
# 2013 All rights reserved to Arbel Zinger, Ehud Tamir

import urllib
from HTMLParser import HTMLParser

KNESSET_URL = "http://www.knesset.gov.il/presence/heb/PresentList.aspx"

class AttendanceHTMLParser(HTMLParser):
    """Parse the Knesset attendence page and extract data in canonical form."""
    def __init__(self):
        HTMLParser.__init__(self)
        self._dict = {}
        self._timestamp = ''

    def handle_starttag(self, tag, attrs):
        """Extract the name and attendence status"""
        if ('class', 'PhotoAsist') in attrs:
            name = self._extract_name(attrs)
            self._dict[name] = True
        elif ('class', 'PhotoAsistno') in attrs:
            name = self._extract_name(attrs)
            self._dict[name] = False

    def handle_data(self, data):
        """Extract the last updated time"""
        label = u'עדכון אחרון:'
        if label.encode('cp1255') in data:
            self._timestamp = data[13:len(data)]

    def get_dict(self):
        return { 'timestamp': self._timestamp,
                  'dictionary': self._dict,
                  }

    def _extract_name(self, attrs):
        return attrs[4][1][19:len(attrs[4][1])-6]

class Attendance(object):
    '''Parse the given URL for Knesset attendance.'''
    def __init__(self, url=KNESSET_URL):
        self._url = url

    def get_attendance(self):
        # Initialize parser
        parser = AttendanceHTMLParser()
        # Read input file
        sock = urllib.urlopen(self._url)
        html_source = sock.read()
        sock.close()
        # Feed to HTML Parser
        parser.feed(html_source)
        return parser.get_dict()

import json
import os
import traceback
import time

BASE = os.path.dirname(os.path.abspath(__file__))
BASE_OUTPUT_DIR = os.path.join(BASE, 'tmp')
LOG_OUTPUT = 'attendance.log'

def main():
    start_time = int(time.time())
    log_string = time.ctime(start_time) + " Starting scrape...\n"
    success = True
    try:
        attendance = Attendance()
        att_dict = attendance.get_attendance()
        if len(att_dict['dictionary']) != 120:
            log_string += "WARNING: Incomplete member list.\n"
    except:
        success = False
        log_string += "ERROR encountered:\n"
        log_string += traceback.format_exc()
        log_string += '\n\n'
    if success:
        out_name = 'attendance-%d' % start_time
        output_file = os.path.join(BASE_OUTPUT_DIR, out_name)
        with open(output_file, 'w') as json_out:
            json.dump(att_dict, json_out)
        log_string += "Output: %s\n" % output_file
    log_file = os.path.join(BASE_OUTPUT_DIR, LOG_OUTPUT)
    with open(log_file, "a") as log:
        log.write(log_string)
    exit(0 if success else -1)

if __name__ == '__main__':
    main()
