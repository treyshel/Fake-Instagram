from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('upload/', views.PhotoView.as_view(), name='upload'),
    path('feed/', views.ShowFeed.as_view(), name='feed')
]
