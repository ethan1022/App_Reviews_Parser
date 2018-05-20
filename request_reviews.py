import requests
import json
import os.path

from os import path

def init():
	file=open(".profile","r")
	if file.mode == "r":
		content = file.read()
		init_dict = json.loads(content)
		return init_dict

def message(dic):
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
				"attachments" : [
					{
						"color":color,
						"pretext":rate_str,
						"title":dic["name"],
						"text":dic["content"],
						"fields":[
							{
								"title":"version",
								"value":dic["version"],
								"short":"true"
							},
							{
								"title":"id",
								"value":dic["identifier"],
								"short":"true"
							}
						]
					}
				],  
				"username":"App Reviews", 
				"mrkdwn": "true"
				}
	return message


def send_slack_message(dic):
	post_data = message(dic)
	headers = {'Content-Type': 'application/json'}
	postResponse = requests.post(url=slack_webhook, headers=headers, data=json.dumps(post_data))

	if postResponse.status_code != 200:
		raise ValueError(
			'Request to slack returned an error %s, the response is:\n%s'
			% (postResponse.status_code, postResponse.text)
			)

def paring_data(data):
	name = data["entry"][1]["author"]["name"]["label"]
	version = data["entry"][1]["im:version"]["label"]
	rate = data["entry"][1]["im:rating"]["label"]
	identifier = data["entry"][1]["id"]["label"]
	content = data["entry"][1]["content"]["label"]
	dic = {"name":name, "version":version, "rate":rate, "identifier":identifier, "content":content}
	return dic

def get_request_data(link):
	getResponse = requests.get(url=link)
	dic = paring_data(json.loads(getResponse.text)["feed"])
	return dic

init_dict = init()
app_reviews_rss_link_tw = init_dict["app_review_rss_link_tw"]
app_reviews_rss_link_jp = init_dict["app_review_rss_link_jp"]
app_reviews_rss_link_us = init_dict["app_review_rss_link_us"]
slack_webhook = init_dict["slack_webhook"]

dic_tw = get_request_data(app_reviews_rss_link_tw)
dic_jp = get_request_data(app_reviews_rss_link_jp)
dic_us = get_request_data(app_reviews_rss_link_us)

id_dic = {
		   "tw":dic_tw["identifier"],
		   "jp":dic_jp["identifier"],
		   "us":dic_us["identifier"]
	     }

if path.exists("review_id.txt"):
	f=open("review_id.txt","r")
	if f.mode == "r":
		content=f.read()
		f=open("review_id.txt","w")
		if content == "":
			f.write(str(id_dic))
		else:
			if content != str(id_dic):
				content_dict = json.loads(content)
				if content_dict["tw"] != id_dic["tw"]:
					send_slack_message(dic_tw)
				if content_dict["jp"] != id_dic["jp"]:
					send_slack_message(dic_jp)
				if content_dict["us"] != id_dic["us"]:
					send_slack_message(dic_us)
				f.write(str(id_dic))
else:
	f=open("review_id.txt", "w+")
	f.write(str(id_dic))
	send_slack_message(dic_tw)
	send_slack_message(dic_jp)
	send_slack_message(dic_us)