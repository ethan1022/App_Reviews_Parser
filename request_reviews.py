#!/usr/bin/env python3

import requests
import json
import os.path
import datetime

from config import config
from os import path

def message(dic, which_country):
	rate = int(dic["rate"])
	color = ""
	if rate > 3:
		color = "#36a64f"
	elif rate == 3:
		color = "#EBB424"
	else:
		color = "#D40E0D"

	rate_str = ""
	for i in range(rate):
		rate_str = rate_str + ":star: "
	message = {
				"icon_emoji": ":apple-icon:",
				"attachments" : [
					{
						"color":color,
						"pretext":rate_str,
						"title":dic["name"],
						"text":dic["content"],
						"fields":[
							{
								"title":"Version",
								"value":dic["version"],
								"short":"true"
							},
							{
								"title":"App Name",
								"value":dic["app_name"],
								"short":"true"
							},
							{
								"title":"Country",
								"value":which_country,
								"short":"true"
							},
							{
								"title":"Date",
								"value":f"{datetime.datetime.now():%Y-%m-%d}",
								"short":"true"
							}
						]
					}
				],  
				"username":"App Reviews", 
				"mrkdwn": "true"
				}
	return message


def send_slack_message(dic, which_country):
	post_data = message(dic, which_country)
	headers = {'Content-Type': 'application/json'}
	postResponse = requests.post(url=slack_webhook, headers=headers, data=json.dumps(post_data))

	if postResponse.status_code != 200:
		raise ValueError(
			'Request to slack returned an error %s, the response is:\n%s'
			% (postResponse.status_code, postResponse.text)
			)

def paring_data(data, index):
	app_name = data[0]["im:name"]["label"]
	name = data[index]["author"]["name"]["label"]
	version = data[index]["im:version"]["label"]
	rate = data[index]["im:rating"]["label"]
	identifier = data[index]["id"]["label"]
	content = data[index]["content"]["label"]
	dic = {"name":name, "version":version, "rate":rate, "identifier":identifier, "content":content, "app_name":app_name}
	return dic

def get_request_data(link):
	getResponse = requests.get(url=link)
	array = json.loads(getResponse.text)["feed"]["entry"]
	return array

def new_review_check(array, which_country, index):
	check_index = index
	review_dic = paring_data(array, check_index)
	current_id = review_dic["identifier"]
	
	if path.exists("review_id_"+ which_country +".txt"):
		f = open("review_id_"+ which_country +".txt", "r")
		if f.mode == "r":
			content = f.read()
			if content == "":
				f.write(current_id)
			else:
				if content != current_id:
					send_slack_message(review_dic, which_country)
					check_index += 1
					new_review_check(array, which_country, check_index)
				else:
					newest_dic = paring_data(array, 1)
					f=open("review_id_"+ which_country +".txt", "w")
					f.write(newest_dic["identifier"])
	else:
		f=open("review_id_"+ which_country +".txt", "w+")
		f.write(current_id)
		send_slack_message(review_dic, which_country)

app_review_rss_link_tw = config["app_review_rss_link_tw"]
app_review_rss_link_jp = config["app_review_rss_link_jp"]
app_review_rss_link_us = config["app_review_rss_link_us"]

slack_webhook = config["slack_webhook"]

review_tw_array = get_request_data(app_review_rss_link_tw)
review_jp_array = get_request_data(app_review_rss_link_jp)
review_us_array = get_request_data(app_review_rss_link_us)

new_review_check(review_tw_array, "tw", 1)
new_review_check(review_jp_array, "jp", 1)
new_review_check(review_us_array, "us", 1)