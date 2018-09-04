from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import *
from random import sample
from django.db import connection

QUESTION_COUNT = 1

def finish(request):
	return HttpResponse("<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'><h1 style='margin-top: 50px'><center>本次答题已结束</center></h1>")

def question(request):
	questions = Question.objects.all()
	# data = {'questions': sample(list(questions), QUESTION_COUNT)}
	data = {'questions': questions}
	return render(request, 'question.html', data)

def submit(request):
	if request.method == "POST":
		questions = Question.objects.all()
		score, count = 0, questions.count()
		for question, answer in request.POST.items():
			if ord(question[0])<65 and questions[int(question)-1].correct == answer:
				score += 1

		score = round(score/count, 2)*100

		student = Student.objects.get(id=request.POST['user_id'])
		student.score = score
		student.status = '1'
		student.save()
		return HttpResponse(json.dumps({"status": 1, "score": score}), content_type="application/json")

def verify(request):
	# if request.method == "POST":
	student = Student.objects.select_related().filter(student_id=request.POST['student_id'])
	if student:
		data = {
			"exist": 1,
			"user_id": student[0].id, 
			"student_name": student[0].student_name,
			"student_id": student[0].student_id,
			"student_department": student[0].student_department.name,
			"student_grade": student[0].student_grade,
		}
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"exist": 0}), content_type="application/json")

def get_answer(request):
	answer_data = []
	cursor = connection.cursor()
	for each in Department.objects.all()[:14]:
		cursor.execute('select count(*), sum(score)/count(*) from start_student where score!=0 and student_department_id=%d' % each.id)
		count, ave = cursor.fetchone()
		answer_rate = min(round(count*100 / each.student_count, 2), 100)
		answer_compre = round(answer_rate*0.7 + ave*0.3, 2)
		answer_data.append([each.name, count, answer_rate, round(ave,2), answer_compre])
	answer_data.sort(key=lambda x:x[4], reverse=True)
	cursor.execute('select count(*), sum(score)/count(*) from start_student where score!=0')
	answer_all_sum, answer_all_ave = cursor.fetchone()
	answer_all_rate = round(answer_all_sum*100 / 17454, 2)
	answer_data.append(['全校', answer_all_sum, answer_all_rate, round(answer_all_ave,2), '--'])
	return HttpResponse(json.dumps(answer_data), content_type="application/json")

def search_all(request):
	return render(request, 'search_all.html')

def search_grade(request):
	cursor = connection.cursor()
	cursor.execute('select distinct student_grade from start_student')
	grades = cursor.fetchall()
	return render(request, 'search_grade.html', {'grades': grades})

def get_grade(request):
	grade = request.GET.get('grade')[2:-3]
	data_grade = []
	cursor = connection.cursor()
	cursor.execute('select count(*), sum(score)/count(*) from start_student where student_grade="%s" and score!=0' % grade)
	data_grade.append(cursor.fetchone())
	cursor.execute('select student_id, student_name, score from start_student where student_grade="%s"' % grade)
	data_grade.extend(cursor.fetchall())
	return HttpResponse(json.dumps(data_grade), content_type="application/json")
