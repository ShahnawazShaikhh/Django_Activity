from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('do_action/', views.do_action, name='do_action'),
    path("do_action1/", views.do_action1, name="do_action1"),
]
