import pandas as pd
import FbApi
import MysqlOperations as ms

def search_news_fb_sources():
	'''
	Read LT_newspapers names from csv LT_newspapers.csv
	and search these names at fb.
	Write raw results at rez.csv:
		- newspaper name
		- newspaper fb id
		- newspaper fb name
	'''
	names_pd = pd.read_csv('csv_files/LT_newspapers.csv')
	newspapers = names_pd['names'].tolist()
	FB_Instance = FbApi.FbApi()
	f = open('csv_files/rez.csv', 'w')
	for newspaper in newspapers:
		json_output = FB_Instance.get_fb_json_callback(FB_Instance.search_url,newspaper)
		for entry in json_output['data']:
			s = '{},{},{} \n' . format(newspaper,entry['id'],entry['name'])
			f.write(s)
	f.close()

def get_post_from_pages(source_table,results_table):
	'''
	Get posts from fb pages
		-source_table is name of table where fb pages are stored
		-results_table is name of table where posts will be stored
	'''
	FB_Instance = FbApi.FbApi()
	mysql_instance = ms.MysqlOperations()
	sql_query = "SELECT * FROM {}" . format(source_table)
	sources = mysql_instance.fetch_obs(sql_query)
	for source in sources:
		print(source['page_name'])
		page_id = source['page_id']
		json_output = FB_Instance.get_fb_json_callback(FB_Instance.posts_url,page_id)
		try:
			json_output['data']
		except KeyError:
			print("page {} doesn't have any posts" . format(source['page_name']))
		else:
			posts_numb = 0
			for entry in json_output['data']:
				entry['created_time'] = FB_Instance.change_fb_timestamp(entry['created_time'])
				entry['page_id'] = page_id
				insertion_rez = mysql_instance.insert_entry_to_posts(results_table,entry)		
				if insertion_rez == "success":
					posts_numb += 1
				elif insertion_rez == "dublication":
					break
		print("{} new posts were inserted" .format(posts_numb))

def get_comments_from_posts(source_table,results_table):
	FB_Instance = FbApi.FbApi()
	mysql_instance = ms.MysqlOperations()
	sql_query = "SELECT * FROM {} where comments_numb <  5".format(source_table)
	posts = mysql_instance.fetch_obs(sql_query)
	for post in posts:
		post_id = post['post_id']
		print("parsing {} post" . format(post_id))
		json_output = FB_Instance.get_fb_json_callback(FB_Instance.post_comments_url,post_id)
		try:
			json_output['comments']['data']
		except KeyError:
			print("post {} doesn't have any comments" . format(post['post_id']))
		else:
			comments_numb = 0
			for entry in json_output['comments']['data']:
				entry['created_time'] = FB_Instance.change_fb_timestamp(entry['created_time'])
				entry['post_id'] = post_id
				try:
					entry['application']
				except KeyError:
					entry['application'] = {'id':None,'namespace':None}
				else:
					insertion_rez = mysql_instance.insert_entry_to_comments(results_table,entry)
					if insertion_rez == "success":
						comments_numb += 1
					elif insertion_rez == "dublication":
						break
			mysql_instance.update_table(source_table,'comments_numb',\
			comments_numb,'post_id',post_id)

if __name__ == "__main__":
	#get_post_from_pages("news_sources","news_posts")
	get_comments_from_posts("news_posts","comments")
