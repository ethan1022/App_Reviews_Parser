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
								"title":"Country",
								"value":which_country,
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
	name = data[index]["author"]["name"]["label"]
	version = data[index]["im:version"]["label"]
	rate = data[index]["im:rating"]["label"]
	identifier = data[index]["id"]["label"]
	content = data[index]["content"]["label"]
	dic = {"name":name, "version":version, "rate":rate, "identifier":identifier, "content":content}
	return dic

def get_request_data(link):
	getResponse = requests.get(url=link)
	array = json.loads(getResponse.text)["feed"]["entry"]
	return array

def new_review_check(array, which_country):
	global check_index
	review_dic = paring_data(array, check_index)
	current_id = review_dic["identifier"]
	
	if path.exists("review_id_"+ which_country +".txt"):
		f = open("review_id_"+ which_country +".txt", "r")
		if f.mode == "r":
			content = f.read()
			f = open("review_id_"+ which_country +".txt", "w")
			if content == "":
				f.write(current_id)
			else:
				if content != current_id:
					send_slack_message(review_dic, which_country)
					check_index = check_index + 1
					new_review_check(array, which_country)
				else:
					check_index = 1
					newest_dic = paring_data(array, check_index)
					f.write(str(newest_dic["identifier"]))
	else:
		f=open("review_id_"+ which_country +".txt", "w+")
		f.write(current_id)
		send_slack_message(review_dic, which_country)



init_dict = init()

check_index = 1

app_reviews_rss_link_tw = init_dict["app_review_rss_link_tw"]
app_reviews_rss_link_jp = init_dict["app_review_rss_link_jp"]
app_reviews_rss_link_us = init_dict["app_review_rss_link_us"]
slack_webhook = init_dict["slack_webhook"]

review_tw_array = get_request_data(app_reviews_rss_link_tw)
review_jp_array = get_request_data(app_reviews_rss_link_jp)
review_us_array = get_request_data(app_reviews_rss_link_us)

new_review_check(review_tw_array, "tw")
new_review_check(review_jp_array, "jp")
new_review_check(review_us_array, "us")