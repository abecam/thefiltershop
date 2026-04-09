from rest_framework import serializers
from filtershop_main.models import (
    Filter, RelatedFilters, TypeOfRelationBetweenFilter,
    ValueForFilter, FiltersForAVideoGameRating,
    Platform, Game_Category, Tag,
    Studio, Publisher, Videogame_common, Videogame_rating,
    Links_to_shops, Image, Online_Shop,
    Review, Profile, Sponsor,
    Recommended_Games_By_Sponsor,
    SteamKey, EmailForGiveAway,
)


# --- Lightweight serializers for nested use ---

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'description']


class GameCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Game_Category
        fields = ['id', 'name', 'description']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'good_or_bad']


class OnlineShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Online_Shop
        fields = ['id', 'name', 'url', 'shop_type']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'title', 'photo']


class LinksToShopsSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source='shop.name', read_only=True)

    class Meta:
        model = Links_to_shops
        fields = ['id', 'link', 'identity', 'shop_name']


# --- Filter serializers ---

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = [
            'id', 'name', 'description', 'is_positive',
            'long_description', 'what_to_change',
        ]


class FilterRelationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeOfRelationBetweenFilter
        fields = ['id', 'name', 'reverse_name', 'both_way']


class RelatedFilterSerializer(serializers.ModelSerializer):
    to_filter = FilterSerializer(read_only=True)
    with_type = FilterRelationTypeSerializer(read_only=True)

    class Meta:
        model = RelatedFilters
        fields = ['to_filter', 'with_type']


class FilterDetailSerializer(serializers.ModelSerializer):
    related_from = RelatedFilterSerializer(source='from_filter', many=True, read_only=True)

    class Meta:
        model = Filter
        fields = [
            'id', 'name', 'description', 'is_positive',
            'long_description', 'what_to_change', 'related_from',
        ]


class ValueForFilterSerializer(serializers.ModelSerializer):
    filter = FilterSerializer(read_only=True)

    class Meta:
        model = ValueForFilter
        fields = ['id', 'value', 'filter']


class FiltersForRatingSerializer(serializers.ModelSerializer):
    filter = FilterSerializer(read_only=True)

    class Meta:
        model = FiltersForAVideoGameRating
        fields = ['id', 'value', 'filter']


# --- Studio / Publisher serializers ---

class StudioListSerializer(serializers.ModelSerializer):
    size_of_studio_display = serializers.CharField(source='get_size_of_studio_display', read_only=True)
    they_have_made_it_display = serializers.CharField(source='get_they_have_made_it_display', read_only=True)

    class Meta:
        model = Studio
        fields = [
            'id', 'name', 'description', 'headline', 'url', 'vignette',
            'general_rating', 'size_of_studio', 'size_of_studio_display',
            'they_have_made_it', 'they_have_made_it_display',
            'known_popularity', 'money_rating', 'fully_rotten',
            'in_hall_of_shame',
        ]


class StudioDetailSerializer(StudioListSerializer):
    tags = TagSerializer(many=True, read_only=True)
    filters = ValueForFilterSerializer(source='valueforfilter_set', many=True, read_only=True)

    class Meta(StudioListSerializer.Meta):
        fields = StudioListSerializer.Meta.fields + [
            'hidden_full_cost', 'description_hidden_full_cost',
            'crapometer', 'descriptionOfShame', 'tags', 'filters',
        ]


class PublisherListSerializer(serializers.ModelSerializer):
    size_of_publisher_display = serializers.CharField(source='get_size_of_publisher_display', read_only=True)
    they_have_made_it_display = serializers.CharField(source='get_they_have_made_it_display', read_only=True)

    class Meta:
        model = Publisher
        fields = [
            'id', 'name', 'description', 'headline', 'url', 'vignette',
            'general_rating', 'size_of_publisher', 'size_of_publisher_display',
            'they_have_made_it', 'they_have_made_it_display',
            'known_popularity', 'money_rating', 'fully_rotten',
            'in_hall_of_shame',
        ]


class PublisherDetailSerializer(PublisherListSerializer):
    tags = TagSerializer(many=True, read_only=True)
    filters = ValueForFilterSerializer(source='valueforfilter_set', many=True, read_only=True)

    class Meta(PublisherListSerializer.Meta):
        fields = PublisherListSerializer.Meta.fields + [
            'hidden_full_cost', 'description_hidden_full_cost',
            'crapometer', 'descriptionOfShame', 'tags', 'filters',
        ]


# --- Videogame rating serializer ---

class VideogameRatingSerializer(serializers.ModelSerializer):
    platform = PlatformSerializer(source='for_platform', read_only=True)
    filters = FiltersForRatingSerializer(source='filtersforavideogamerating_set', many=True, read_only=True)

    class Meta:
        model = Videogame_rating
        fields = [
            'id', 'name', 'platform', 'same_platform_alternative_shop',
            'f2play', 'f2pay',
            'gameplay_rating', 'money_rating',
            'good_wo_iap', 'good_wo_ads', 'ads_supported',
            'fully_rotten', 'use_psycho_tech', 'crapometer',
            'would_be_good_if', 'could_be_good_if',
            'filters',
        ]


# --- Videogame serializers ---

class VideogameListSerializer(serializers.ModelSerializer):
    studios = StudioListSerializer(many=True, read_only=True)
    publishers = PublisherListSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    categories = GameCategorySerializer(many=True, read_only=True)
    they_have_made_it_display = serializers.CharField(source='get_they_have_made_it_display', read_only=True)

    class Meta:
        model = Videogame_common
        fields = [
            'id', 'name', 'description', 'headline', 'url', 'vignette',
            'general_rating', 'gameplay_rating', 'game_type',
            'they_have_made_it', 'they_have_made_it_display',
            'in_the_spotlight', 'known_popularity',
            'link_sold_from_dev', 'special_bonuses',
            'are_special_bonuses_global', 'general_sale',
            'studios', 'publishers', 'platforms', 'categories',
            'in_hall_of_shame',
        ]
        # special_sale is intentionally excluded


class VideogameDetailSerializer(VideogameListSerializer):
    tags = TagSerializer(many=True, read_only=True)
    filters = ValueForFilterSerializer(source='valueforfilter_set', many=True, read_only=True)
    ratings = VideogameRatingSerializer(source='videogame_rating_set', many=True, read_only=True)
    images = ImageSerializer(source='image_set', many=True, read_only=True)
    shop_links = LinksToShopsSerializer(source='links_to_shops_set', many=True, read_only=True)

    class Meta(VideogameListSerializer.Meta):
        fields = VideogameListSerializer.Meta.fields + [
            'hidden_full_cost', 'description_hidden_full_cost',
            'crapometer', 'descriptionOfShame',
            'tags', 'filters', 'ratings', 'images', 'shop_links',
        ]


# --- Review serializers ---

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='profile.full_name', read_only=True)
    game_name = serializers.CharField(source='game.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer_name', 'game', 'game_name',
            'review_txt', 'note', 'date_creation',
        ]


# --- Profile / Curator serializers ---

class CuratorSerializer(serializers.ModelSerializer):
    contribution_level_display = serializers.CharField(source='get_contribution_level_display', read_only=True)
    recommended_games = VideogameListSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'full_name', 'biography', 'avatar',
            'contribution_level', 'contribution_level_display',
            'number_of_contrib', 'nb_of_articles',
            'recommended_games',
        ]


# --- Sponsor serializers ---

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = [
            'id', 'name', 'description', 'url', 'sponsor_logo',
            'in_hall_of_shame',
        ]


class SponsorRecommendationSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer(read_only=True)
    game = VideogameListSerializer(read_only=True)

    class Meta:
        model = Recommended_Games_By_Sponsor
        fields = ['id', 'sponsor', 'game', 'review_txt', 'note']


# --- Giveaway serializer ---

class GiveawayEntrySerializer(serializers.Serializer):
    email = serializers.EmailField()


# --- Search result serializer ---

class SearchResultSerializer(serializers.Serializer):
    games = VideogameListSerializer(many=True, read_only=True)
    studios = StudioListSerializer(many=True, read_only=True)
    publishers = PublisherListSerializer(many=True, read_only=True)
    filters = FilterSerializer(many=True, read_only=True)
