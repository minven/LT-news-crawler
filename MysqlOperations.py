import pymysql.cursors
import yaml


class MysqlOperations:
	def __init__(self):
		with open("config.yml", 'r') as ymlfile:
		    cfg = yaml.load(ymlfile)['mysql_login']
		connection = pymysql.connect(host='localhost',
		                             user='root',
		                             password=cfg['password'],
		                             db=cfg['db_name'],
		                             charset=cfg['charset'],
		                             cursorclass=pymysql.cursors.DictCursor)
		self.connection = connection

	def fetch_obs(self,sql_query):
		cursor = self.connection.cursor()
		cursor.execute(sql_query)
		result = cursor.fetchall()
		return result
	def insert_entry_to_posts(self,table_name,entry):
		'''
	    page_id varchar(50) not null,
	    post_id varchar(50) not null,
	    post_time datetime DEFAULT NULL,
	    post varchar(1024) not null,
	    post_url varchar(255) not null,
	    fb_post_url varchar(255) not null,
	    comments_numb int(4) default 0,
		'''
		sql = "INSERT INTO {} (page_id,post_id,post_time,post,post_url,fb_post_url,comments_numb)"\
		 "VALUES (%s,%s,%s,%s,%s,%s,%s)" . format(table_name)
		cursor = self.connection.cursor()
		try:
			cursor.execute(sql, (entry['page_id'],entry['id'],\
				entry['created_time'],entry['message'],entry['link'],entry['actions'][0]['link'],0))
		except pymysql.err.IntegrityError:
			print("post with id = {} is duplication in db" . format(entry['id']))
			return "dublication"
		except:
			print("post with id = {} was not inserted due to unknown error" . format(entry['id']))
			return 0
		else:
			self.connection.commit()
			return "success"
	def insert_entry_to_comments(self,table_name,entry):
		'''
	    post_id varchar(50) not null,
	    comment_id varchar(50) not null,
	    commenter varchar(100) not null,
	    commenter_id varchar(50) not null,
	    comment_time datetime DEFAULT NULL,
	    comment varchar(1024) not null,
	    comment_count int(3) DEFAULT 0,
	    comment_likes int(5) DEFAULT 0,
	    app_name varchar(20) DEFAULT NULL,
	    app_id varchar(50) DEFAULT NULL, 
		'''
		sql = "INSERT INTO comments (post_id,comment_id,commenter,commenter_id,comment_time," \
		"comment,comment_count,comment_likes,app_name,app_id)"\
		 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" . format(table_name)
		cursor = self.connection.cursor()
		try:
			cursor.execute(sql, (entry['post_id'],entry['id'],entry['from']['name'],entry['from']['id'],\
				entry['created_time'],entry['message'],entry['comment_count'],entry['like_count'],\
				entry['application']['namespace'],entry['application']['id']))
		except pymysql.err.IntegrityError:
			print("comment with id = {} is duplication in db" . format(entry['id']))
			return "dublication"
		except:
			print("comment with id = {} was not inserted due to unknown error" . format(entry['id']))
			return 0
		else:
			self.connection.commit()
			return "success"
	def update_table(self,table_name,s_key,s_val,w_key,w_value):
		'''
		update mysql table
		'''
		sql = "update {} set {} = {} where {} = '{}'".\
		format(table_name,s_key,s_val,w_key,w_value)
		cursor = self.connection.cursor()
		try:
			cursor.execute(sql)
		except:
			print("comment_numb update error")
		else:
			self.connection.commit()
			print("{} comments where inserted successfully\n" . format(s_val))	
if __name__ == "__main__":
	pass