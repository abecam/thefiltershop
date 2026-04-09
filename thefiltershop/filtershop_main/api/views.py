from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

from filtershop_main.models import (
    Filter, Platform, Game_Category,
    Studio, Publisher, Videogame_common, Videogame_rating,
    Review, Profile, Sponsor, Recommended_Games_By_Sponsor,
)
from filtershop_main.api.serializers import (
    FilterSerializer, FilterDetailSerializer,
    PlatformSerializer, GameCategorySerializer,
    StudioListSerializer, StudioDetailSerializer,
    PublisherListSerializer, PublisherDetailSerializer,
    VideogameListSerializer, VideogameDetailSerializer,
    VideogameRatingSerializer,
    ReviewSerializer,
    CuratorSerializer, SponsorSerializer,
    SponsorRecommendationSerializer,
    SearchResultSerializer,
)


class FilterViewSet(viewsets.ReadOnlyModelViewSet):
    """Filters (positive and negative quality attributes)."""
    queryset = Filter.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FilterDetailSerializer
        return FilterSerializer

    @action(detail=False, url_path='positive')
    def positive(self, request):
        qs = self.queryset.filter(is_positive=True)
        return Response(FilterSerializer(qs, many=True).data)

    @action(detail=False, url_path='negative')
    def negative(self, request):
        qs = self.queryset.filter(is_positive=False)
        return Response(FilterSerializer(qs, many=True).data)


class PlatformViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [AllowAny]


class GameCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game_Category.objects.all()
    serializer_class = GameCategorySerializer
    permission_classes = [AllowAny]


class StudioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Studio.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudioDetailSerializer
        return StudioListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        size = self.request.query_params.get('size')
        if size:
            qs = qs.filter(size_of_studio=size.upper())
        return qs


class PublisherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publisher.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PublisherDetailSerializer
        return PublisherListSerializer


class VideogameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Video games with filtering by studio size, category, and platform.

    Query params:
    - studio_size: AR, IN, ME, BI, HU
    - category: category id
    - platform: platform id
    """
    queryset = Videogame_common.objects.all().order_by('-general_rating')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VideogameDetailSerializer
        return VideogameListSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        studio_size = self.request.query_params.get('studio_size')
        if studio_size:
            qs = qs.filter(studios__size_of_studio=studio_size.upper()).distinct()

        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(categories__id=category)

        platform = self.request.query_params.get('platform')
        if platform:
            qs = qs.filter(platforms__id=platform)

        return qs

    @action(detail=False, url_path='artisans')
    def artisans(self, request):
        """Games from artisan studios (5 or fewer people)."""
        qs = self.queryset.filter(studios__size_of_studio='AR').distinct()
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                VideogameListSerializer(page, many=True, context={'request': request}).data
            )
        return Response(VideogameListSerializer(qs, many=True, context={'request': request}).data)

    @action(detail=False, url_path='indies')
    def indies(self, request):
        """Games from indie studios."""
        qs = self.queryset.filter(studios__size_of_studio='IN').distinct()
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                VideogameListSerializer(page, many=True, context={'request': request}).data
            )
        return Response(VideogameListSerializer(qs, many=True, context={'request': request}).data)

    @action(detail=False, url_path='made-it')
    def made_it(self, request):
        """Artisan/indie games that achieved commercial success."""
        qs = self.queryset.filter(
            they_have_made_it__in=['YE', 'ME', 'MA']
        ).filter(
            Q(studios__size_of_studio__in=['AR', 'IN'])
        ).distinct()
        return Response(VideogameListSerializer(qs, many=True, context={'request': request}).data)

    @action(detail=False, url_path='best-of-rest')
    def best_of_rest(self, request):
        """High-quality games that meet strict ethical criteria."""
        rating_ids = Videogame_rating.objects.filter(
            gameplay_rating__gt=80,
            good_wo_iap__gt=80,
            good_wo_ads__gt=80,
            use_psycho_tech=0,
        ).values_list('Videogame_common_id', flat=True)
        qs = self.queryset.filter(id__in=rating_ids)
        return Response(VideogameListSerializer(qs, many=True, context={'request': request}).data)

    @action(detail=False, url_path='random-artisan')
    def random_artisan(self, request):
        """Random unfiltered artisan game."""
        game = self.queryset.filter(
            studios__size_of_studio='AR'
        ).exclude(
            valueforfilter__filter__is_positive=False
        ).order_by('?').first()
        if not game:
            return Response({'detail': 'No matching game found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(VideogameDetailSerializer(game, context={'request': request}).data)

    @action(detail=False, url_path='random-indie')
    def random_indie(self, request):
        """Random unfiltered indie game."""
        game = self.queryset.filter(
            studios__size_of_studio='IN'
        ).exclude(
            valueforfilter__filter__is_positive=False
        ).order_by('?').first()
        if not game:
            return Response({'detail': 'No matching game found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(VideogameDetailSerializer(game, context={'request': request}).data)

    @action(detail=True, url_path='reviews')
    def reviews(self, request, pk=None):
        """Reviews for a specific game."""
        reviews = Review.objects.filter(game_id=pk)
        return Response(ReviewSerializer(reviews, many=True).data)


class HallOfShameViewSet(viewsets.GenericViewSet):
    """Entities in the Hall of Shame."""
    permission_classes = [AllowAny]

    def list(self, request):
        games = Videogame_common.objects.filter(in_hall_of_shame=True)
        studios = Studio.objects.filter(in_hall_of_shame=True)
        publishers = Publisher.objects.filter(in_hall_of_shame=True)
        sponsors = Sponsor.objects.filter(in_hall_of_shame=True)
        return Response({
            'games': VideogameListSerializer(games, many=True, context={'request': request}).data,
            'studios': StudioListSerializer(studios, many=True, context={'request': request}).data,
            'publishers': PublisherListSerializer(publishers, many=True, context={'request': request}).data,
            'sponsors': SponsorSerializer(sponsors, many=True, context={'request': request}).data,
        })


class CuratorViewSet(viewsets.ReadOnlyModelViewSet):
    """Curators and contributors."""
    queryset = Profile.objects.exclude(
        contribution_level='RE'
    ).order_by('-number_of_contrib')
    serializer_class = CuratorSerializer
    permission_classes = [AllowAny]


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [AllowAny]


class SponsorRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recommended_Games_By_Sponsor.objects.select_related('sponsor', 'game')
    serializer_class = SponsorRecommendationSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
def search(request):
    """Search across games, studios, publishers, and filters."""
    q = request.query_params.get('q', '').strip()
    if len(q) < 3:
        return Response(
            {'detail': 'Search query must be at least 3 characters.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = {
        'games': VideogameListSerializer(
            Videogame_common.objects.filter(name__icontains=q), many=True, context={'request': request}
        ).data,
        'studios': StudioListSerializer(
            Studio.objects.filter(name__icontains=q), many=True, context={'request': request}
        ).data,
        'publishers': PublisherListSerializer(
            Publisher.objects.filter(name__icontains=q), many=True, context={'request': request}
        ).data,
        'filters': FilterSerializer(
            Filter.objects.filter(name__icontains=q), many=True
        ).data,
    }
    return Response(data)
