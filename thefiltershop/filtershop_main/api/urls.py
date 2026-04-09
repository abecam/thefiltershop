from django.urls import path, include
from rest_framework.routers import DefaultRouter
from filtershop_main.api import views

router = DefaultRouter()
router.register(r'games', views.VideogameViewSet, basename='game')
router.register(r'studios', views.StudioViewSet, basename='studio')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'filters', views.FilterViewSet, basename='filter')
router.register(r'platforms', views.PlatformViewSet, basename='platform')
router.register(r'categories', views.GameCategoryViewSet, basename='category')
router.register(r'hall-of-shame', views.HallOfShameViewSet, basename='hall-of-shame')
router.register(r'curators', views.CuratorViewSet, basename='curator')
router.register(r'sponsors', views.SponsorViewSet, basename='sponsor')
router.register(r'sponsor-recommendations', views.SponsorRecommendationViewSet, basename='sponsor-recommendation')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.search, name='api-search'),
]
