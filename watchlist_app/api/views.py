from django.forms import ValidationError as DRFValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend

from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Reviews
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        # Filtering using paramaters:
        # username = self.request.query_params.get('username')
        return Reviews.objects.filter(review_user__username=username)
        '''
        Why We Need to Append __<field> After Foreign Keys:
            1. Accessing Related Model Fields: The double underscore __ allows you to access fields of the related model (in this case, User).
            2. Following Relationships: When working with foreign key relationships, __ enables Django to follow that relationship and access the fields of the related model.
            3. Chaining Field Lookups: You can chain lookups through multiple relationships. For example, if User had a related profile with its own fields, you could chain lookups like review_user__profile__bio.
        '''


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise DRFValidationError({"detail": "You have already reviewed this Movie"})

        rating = serializer.validated_data['rating']

        # Update number_rating first
        watchlist.number_rating += 1

        # Recalculate the average rating
        watchlist.avg_rating = ((watchlist.avg_rating * (watchlist.number_rating - 1)) + rating) / watchlist.number_rating

        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    #Custom throttle scope
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-list'
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)


class WatchListFilter(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']

class WatchListSearch(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'avg_rating' , 'platform__name']


class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    serializer_class = ReviewSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    queryset = Reviews.objects.all()

    def get(self, request, *args, **kwargs):
        print(f"User: {request.user}")
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class WatchListAV(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class WatchDetailAV(APIView):

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
             return Response({'Error': 'WatchList does not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformListAV(APIView):

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'This id is incorrect'})

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def movie_list(request):

#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):

#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)

#         except Movie.DoesNotExist:
#             return Response({'Error': 'Movie does not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
