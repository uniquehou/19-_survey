from django.contrib import admin
from .models import *
from django.db import connection

class StudentAdmin(admin.ModelAdmin):
	list_display = ('student_name', 'student_id', 'student_department', 'student_grade', 'score')
	list_filter = ['student_department', 'student_grade']
	# readonly_fields = []
	search_fields = ('score', 'student_name')
	# raw_id_fields = ()
	# list_per_page = 20


class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'aver', 'student_count')


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question_text', 'correct')


admin.site.register(Student, StudentAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Question, QuestionAdmin)
