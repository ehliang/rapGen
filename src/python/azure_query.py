import requests
import copy
import json

class Requests():
	def __init__(self):
		self.headers = {
    	# Request headers
    	'Ocp-Apim-Subscription-Key': '1436916bb4714c2baf7d21f1b96dbfb2'
		}
		self.params = {'model': 'body', 'order':5}

	def next_word(self, string):
		url = "https://api.projectoxford.ai/text/weblm/v1.0/generateNextWords"
		params = copy.deepcopy(self.params)
		params['words'] = string
		params['maxNumOfCandidatesReturned'] = 15
		resp = requests.post(url, params = params, headers = self.headers)
		resp_dict = json.loads(resp.text)
		#print string, resp_dict
		max_prob = max([x["probability"] for x in resp_dict["candidates"]])
		for i, word in enumerate(resp_dict["candidates"]):
			if max_prob == word["probability"]:
				arg_max = i
				break
		k = str(resp_dict["candidates"][arg_max]['word'])
		if k[0] >='0' and k[0] <= '9' or k in ['fuck', 'porn']:
			raise 'invalid'
		return string + " " + resp_dict["candidates"][arg_max]['word']

	def next_prob(self, string, word_list):
		url = 'https://api.projectoxford.ai/text/weblm/v1.0/calculateConditionalProbability'
		data = {"queries":[]}
		for word in word_list:
			data["queries"].append({"words":string, "word":word})
		params = self.params
		headers = copy.deepcopy(self.headers)
		headers['Content-Type'] = 'application/json'
		resp = requests.post(url, params = params, headers = headers, data = json.dumps(data))
		resp_dict = json.loads(resp.text)
		if "results" not in resp_dict: return string
		max_prob = max([x["probability"] for x in resp_dict["results"]])
		for i, word in enumerate(resp_dict["results"]):
			if max_prob == word["probability"]:
				arg_max = i
				break
		return string + " " + resp_dict["results"][arg_max]['word']

	def validate(self, string):
		url = "https://api.projectoxford.ai/text/weblm/v1.0/calculateJointProbability"
		data = {"queries":[string]}
		params = self.params
		headers = copy.deepcopy(self.headers)
		headers['Content-Type'] = 'application/json'
		resp = requests.post(url, params = params, headers = headers, data = json.dumps(data))
		resp_dict = json.loads(resp.text)
		#print resp_dict
		results = resp_dict['results']
		return results[0]['probability']

if __name__ == "__main__":
	l = Requests()
	print l.validate("Today is a good day")