from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    release_year = models.IntegerField()

    def __str__(self):
        return self.title

class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'movie')

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = '__all__'

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def rate_movie(self, request, pk=None):
        movie = get_object_or_404(Movie, pk=pk)
        rating = request.data.get('rating')
        if not rating or int(rating) not in range(1, 6):
            return Response({"error": "Rating must be between 1 and 5"}, status=400)
        
        movie_rating, created = MovieRating.objects.update_or_create(
            user=request.user, movie=movie, defaults={'rating': rating}
        )
        return Response({"message": "Rating saved"})

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        user_ratings = MovieRating.objects.filter(user=request.user)
        if not user_ratings.exists():
            return Response({"message": "No ratings found. Rate movies to get recommendations."})
        
        liked_genres = Movie.objects.filter(ratings__in=user_ratings.filter(rating__gte=4)).values_list('genre', flat=True).distinct()
        recommended_movies = Movie.objects.filter(genre__in=liked_genres).exclude(ratings__user=request.user)
        serializer = MovieSerializer(recommended_movies, many=True)
        return Response(serializer.data)

class MovieRatingViewSet(viewsets.ModelViewSet):
    queryset = MovieRating.objects.all()
    serializer_class = MovieRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'ratings', MovieRatingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
