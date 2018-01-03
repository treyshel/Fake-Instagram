from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('upload/', views.PhotoView.as_view(), name='upload'),
    path('feed/', views.ShowFeed.as_view(), name='feed'),
    path('filter/<image_id>/', views.AddFilter.as_view(), name='filter'),
    path('delete/<image_id>', views.DeletePost.as_view(), name='delete'),
    path('comment/<image_id>', views.AddComment.as_view(), name='comment'),
    path('likes/<image_id>', views.Like.as_view(), name='likes')
]
