# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
import json
import requests

def send_to_slack(message):
	slackURL = "URL"
	requests.post(slackURL, data = json.dumps({
		'text': message,
		'username': u'mercari-bot',
		'link_names': 1
	}))
