from django.urls import path
# from watchlist_app.api.views import movie_list, movie_details
from watchlist_app.api.views import WatchListAV, WatchDetailAV, StreamPlatformListAV, StreamPlatformDetailAV, ReviewList, ReviewDetail, ReviewCreate, UserReview, WatchListFilter, WatchListSearch

urlpatterns = [
    path("list/", WatchListAV.as_view(), name="movie-list"),
    path("<int:pk>/", WatchDetailAV.as_view(), name="movie-detail"),
    path('streamlist/', StreamPlatformListAV.as_view(), name='stream-list'),
    path('streamlist/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream-platform-details'),
    path('list2/', WatchListFilter.as_view(), name='watchlist-filter'),
    path('list-search/', WatchListSearch.as_view(), name='watchlist-search'),
    # path('review/', ReviewList.as_view(), name="review-list"),
    # path('review/<int:pk>', ReviewDetail.as_view(), name="review-detail"),
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('reviews/<str:username>/', UserReview.as_view(), name='user-review'),
]
