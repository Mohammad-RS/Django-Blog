from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('posts/',views.PostsListView.as_view(), name='posts'), 
    path('read-later/',views.ReadLaterView.as_view(), name='saved'),
    path('<slug:slug>/',views.PostDetailsView.as_view(), name='post_details'), 
    path('<slug:slug>/read-later/',views.ReadLaterView.as_view(), name='read_later'),
    path('author/<str:first_name>-<str:last_name>/',views.AuthorInfoView.as_view(), name='author_info'),
]
