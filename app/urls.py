from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'
urlpatterns = [
    path('feed', views.ShowFeed.as_view(), name='feed'),
    path('upload/', views.PhotoView.as_view(), name='upload'),
    path('filter/<image_id>/', views.AddFilter.as_view(), name='filter'),
    path('delete/<image_id>', views.DeletePost.as_view(), name='delete'),
    path('comment/<image_id>', views.AddComment.as_view(), name='comment'),
    path('likes/<image_id>', views.Like.as_view(), name='likes'),
    path('mostpopular/', views.MostPopular.as_view(), name='mostpopular'),
    path('topics/<topic_id>', views.GetTopic.as_view(), name='topics'),
    path(
        'buzzingcomments/',
        views.BuzzingComments.as_view(),
        name='buzzingcomments'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', auth_views.logout, name='logout'),
    path('', views.Login.as_view(), name='login'),
]
