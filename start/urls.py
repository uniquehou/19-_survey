from django.conf.urls import url
from . import views

app_name="start"
urlpatterns = [
	url(r'^question/', views.question, name="question"),
	url(r'^verify/', views.verify, name="verify"),
	url(r'^submit/', views.submit, name='submit'),
	url(r'^search_all/', views.search_all, name='search_all'),
	url(r'^get_answer/', views.get_answer, name='get_answer'),
	url(r'^search_grade/', views.search_grade, name='search_grade'),
	url(r'^get_grade/', views.get_grade, name='get_grade'),
]
