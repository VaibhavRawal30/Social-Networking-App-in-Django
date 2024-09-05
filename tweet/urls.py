from django.urls import path
from .views import tweet_list, tweet_create, tweet_edit, tweet_delete, register, tweet_detail, delete_comment, add_comment, like_tweet
urlpatterns = [
    path('',tweet_list, name = "tweet_list"),
    path('create/',tweet_create, name = "tweet_create"),
    path('<int:tweet_id>/edit/',tweet_edit, name = "tweet_edit"),
    path('<int:tweet_id>/delete/',tweet_delete, name = "tweet_delete"),
    path('register/', register, name = 'register'),

    path('tweet/<int:tweet_id>/', tweet_detail, name='tweet_detail'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('add_comment/<int:tweet_id>/', add_comment, name='add_comment'),
    path('tweet/like/<int:tweet_id>/', like_tweet, name='like_tweet'),
    
]
