departments = {
	'文学院': 1 ,
	'外国语学院': 2 ,
	'政治与历史学院': 3 ,
	'教育科学与技术学院': 4 ,
	'数理学院': 5 ,
	'生物科学与技术学院': 6 ,
	'化学化工学院': 7 ,
	'信息技术与工程学院': 8 ,
	'音乐学院': 9 ,
	'体育学院': 10 ,
	'美术学院': 11 ,
	'机械学院': 12 ,
	'经济管理学院': 13 ,
	'旅游与公共管理学院': 14 ,
	'公共管理学院': 14,
	'远程教育学院': 15 ,
	'继续教育学院': 16 ,
}
error = []

import xlrd
wb = xlrd.open_workbook("17.xls")
table = wb.sheets()[0]
nrows = table.nrows
for row in range(1,10):
	data = table.row_values(row)[2:]
	data[2] = departments[data[2]]
	print(tuple(data))

import pymysql
conn = pymysql.connect(host="localhost", port=3306, user='root', password='mysqlrootpndc', db='survey', charset='utf8')
cursor = conn.cursor()

for row in range(1, nrows):
	data = table.row_values(row)[2:]
	data[2] = departments[data[2]]
	try:
		sql = "insert into start_student(student_id, student_name, student_department_id, student_grade, score) values('%s', '%s', %d, '%s', 0)" % tuple(data)
		row = cursor.execute(sql)
#		print("insert", data)
	except pymysql.err.IntegrityError:
		sql = "update start_student set student_name='%s', student_department_id=%d, student_grade='%s' where student_id='%s'" % tuple(data[1:]+[data[0]])
		print('error: ', data)
		row = cursor.execute(sql)
		error.append(data)
	conn.commit()

cursor.close()
conn.close()

print("error: ", len(error))


# insert start_department(name, id) values('文学院', 1);
# insert start_department(name, id) values('外国语学院', 2);
# insert start_department(name, id) values('政治与历史学院', 3);
# insert start_department(name, id) values('教育科学与技术学院', 4);
# insert start_department(name, id) values('数理学院', 5);
# insert start_department(name, id) values('生物科学与技术学院', 6);
# insert start_department(name, id) values('化学化工学院', 7);
# insert start_department(name, id) values('信息技术与工程学院', 8);
# insert start_department(name, id) values('音乐学院', 9);
# insert start_department(name, id) values('体育学院', 10);
# insert start_department(name, id) values('美术学院', 11);
# insert start_department(name, id) values('机械学院', 12);
# insert start_department(name, id) values('经济管理学院', 13);
# insert start_department(name, id) values('旅游与公共管理学院', 14);
# insert start_department(name, id) values('远程教育学院', 15);
# insert start_department(name, id) values('继续教育学院', 16);
