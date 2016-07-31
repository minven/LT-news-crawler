import yaml
import json
import urllib.request
import urllib.parse
import time
class FbApi:
	def __init__(self):
		'''
		Get fb graph api authentication key form yaml
		'''
		with open("config.yml", 'r') as ymlfile:
		    cfg = yaml.load(ymlfile)
		self.auth_key = cfg['auth_key']
	def get_fb_json_callback(self,func_create_url,fb_id):
		url = func_create_url(fb_id,self.auth_key)
		url_output = self.get_html_from_url(url)
		try:
			json_output = json.loads(url_output)
		except:
			print("fb posts json wasn't loaded successfully")
		return json_output		

	def get_html_from_url(self,url):
		mystr = ""
		try:
			fp = urllib.request.urlopen(url)
			mybytes = fp.read()
			#convert html bytes format to utf8 string
			mystr = mybytes.decode("utf8",errors = "ignore")
		finally:
			fp.close()
			return mystr
	def change_fb_timestamp(self,fb_timestamp):
		time_obj = time.strptime(fb_timestamp, '%Y-%m-%dT%H:%M:%S+0000')
		time_str = time.strftime('%Y-%m-%d %H:%I:%S', time_obj)
		return time_str
	def search_url(self,name,auth_key):
		return "https://graph.facebook.com/v2.7/search?q={}&type=page&access_token={}" .\
		format(urllib.parse.quote(name),auth_key)
	def posts_url(self,page_id,auth_key):
		return "https://graph.facebook.com/v2.7/{}/posts?fields=message,actions,link,created_time&limit=100&access_token={}" .\
		format(page_id,auth_key)
	def post_comments_url(self,post_id,auth_key):
		return "https://graph.facebook.com/v2.7/{}?fields=comments.limit(500)" \
		"%7Blike_count,message,created_time,application,comment_count,from,user_likes%7D&access_token={}".\
		format(post_id,auth_key)
if __name__ == "__main__":
	pass