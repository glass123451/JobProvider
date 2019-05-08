from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('mylogin/', views.mylogin, name='mylogin'),
    path('mylogout/', views.mylogout, name='mylogout'),
    path('search_job/', views.search_job, name='search_job'),
    path('job_detail/<int:job_id>/', views.job_detail, name="job_detail"),
    path('apply/<int:job_id>/', views.apply, name="apply"),
    path('manage_job/', views.manage_job, name='manage_job'),
    path('search_unemp/', views.search_unemp, name='search_unemp'),
    path('unemp_detail/<int:unemp_id>/', views.unemp_detail, name="unemp_detail"),
    path('offer/<int:unemp_id>/<int:job_id>/', views.offer, name="offer"),
    path("register_student/", views.register_student, name="register_student"),
    path("register_employer/", views.register_employer, name="register_employer"),
    path("edit_employer/", views.edit_employer, name="edit_employer"),
    path("delete/<int:job_id>/", views.delete, name="delete"),
    path("change/", views.change, name="change"),
    path("add_req/<int:job_id>/", views.add_req, name="add_req"),
    path("edit_student/", views.edit_student, name="edit_student"),
    path("delete_skill/<int:skill_id>/", views.delete_skill, name="delete_skill"),
    path("add_skill/", views.add_skill, name="add_skill"),
]