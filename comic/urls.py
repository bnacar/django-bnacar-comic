from django.urls import path

from . import views

app_name = 'comic'
urlpatterns = [
    path('<slug:title_slug>/', views.index, name='index'),
    path('<slug:title_slug>/<int:episode_num>/', views.episode, name='episode'),
    path('<slug:title_slug>/tags/<slug:tag_slug>/', views.tag, name='tag')
]

