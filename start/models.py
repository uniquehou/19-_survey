from django.db import models

class Department(models.Model):
	name = models.CharField(u'院系名', max_length=100)
	aver = models.FloatField(u'平均分', default=0)
	student_count = models.SmallIntegerField(u'填写学生数', default=0)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '院系'
		verbose_name_plural = '院系'


class Student(models.Model):
	status_choice = (
		('0', '未答'),
		('1', '已答')
	)

	student_name = models.CharField(u'姓名', max_length=30, default=' ')
	student_id = models.CharField(u'学号', max_length=20, default=' ', unique=True)
	student_department = models.ForeignKey("Department", on_delete=models.SET_NULL, verbose_name='院系', default=0, null=True)
	student_grade = models.CharField(u'班级', max_length=60, default=' ')
	student_status = models.CharField(u'是否已答题', max_length=2, default='0', blank=True, choices=status_choice);
	score = models.FloatField(u'得分', default=0)

	def __str__(self):
		return self.student_name

	class Meta:
		verbose_name = '学生'
		verbose_name_plural = '学生'


class Question(models.Model):
	correct_choice = (
		('1', '选项1'),
		('2', '选项2'),
		('3', '选项3'),
		('4', '选项4'),
	)

	question_text = models.CharField(u'问题', max_length=1000, default=' ')
	answer_1 = models.CharField(u'选项1', max_length=1000, default=' ')
	answer_2 = models.CharField(u'选项2', max_length=1000, default=' ')
	answer_3 = models.CharField(u'选项3', max_length=1000, default=' ')
	answer_4 = models.CharField(u'选项4', max_length=1000, default=' ')
	correct = models.CharField(u'正确选项', max_length=1, default='0', choices=correct_choice)

	def __str__(self):
		return self.question_text

	class Meta:
		verbose_name = '问题'
		verbose_name_plural = '问题'
