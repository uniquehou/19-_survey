from tornado import ioloop, web, gen
from tornado_mysql import pools
import pymysql
from random import sample
import json

settings = {
	"cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
}

POOL = pools.Pool(
	dict(host='localhost', port=3306, user='root', passwd='root', db='survey', charset="utf8"),
	max_idle_connections=100,
	max_recycle_sec=5)

def mysql_query(sql):
	conn = pymysql.connect(**settings['db_config'])
	cursor = conn.cursor()

	cursor.execute(sql)
	rows = cursor.fetchall()
	conn.commit()

	cursor.close()
	conn.close()
	return rows

def mysql_insert(sql):
	conn = pymysql.connect(**settings['db_config'])
	cursor = conn.cursor()

	row = cursor.execute(sql)
	conn.commit()

	cursor.close()
	conn.close()
	return row

def search_student(student_id):
	return {"exist": 1, "user_id": '1', "student_name": "侯亚杰", "student_id": "1511112112", "student_department": "信息工程与技术学院", "student_grade": "计算机科学与技术"}
	# return {"exist": 0}

class MainHandler(web.RequestHandler):
	@web.asynchronous
	@gen.coroutine
	def get(self):
		questions = yield POOL.execute("select * from start_question")
		self.render("templates/question.html", questions=questions )


class VerifyHandler(web.RequestHandler):
	def post(self):
		student_id = self.get_argument("student_id")
		student = search_student(student_id)
		self.write(json.dumps(student))
		self.finish()


class SubmitHandler(web.RequestHandler):
	def post(self):
		# questions = mysql_query("select * from start_question")
		# score, count = 0, 0
		# for question in questions:
		# 	if self.get_argument(question.id) == question.correct:
		# 		score += 1
		# 	count += 1
		# score = round(score/count, 2)*100

		# user_id = self.get_argument("user_id")
		# update_sql = "update start_student set score={0} where id={1}"
		# mysql_insert(sql.format(score, user_id))
		self.write(json.dumps({"status": 1, "score": 50}))
		

application = web.Application([
	(r"/question", MainHandler),
	(r"/verify", VerifyHandler),
	(r"/submit", SubmitHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	ioloop.IOLoop.instance().start()
	# questions = mysql_query("select * from start_question")
	# print(questions)