from io import BytesIO
from unittest.mock import patch

from django.test import TestCase

from .admin import EntryOnSteam
from .models import Entry_on_Steam, TypeOfEntity, Videogame_common


class SteamAdminTests(TestCase):
    def test_get_review_count_uses_stored_videogame_id_when_name_differs(self):
        entity_type = TypeOfEntity.objects.create(name="Video Game")
        game = Videogame_common.objects.create(name="Real Game", for_type=entity_type)
        entry = Entry_on_Steam.objects.create(
            appid=12345,
            name="Different Manual Name",
            videogame=game,
        )

        class DummyAdmin:
            def message_user(self, request, message):
                return None

        html = b'<html><body><span itemprop="reviewCount" content="42"></span></body></html>'

        class DummyResponse:
            def __enter__(self):
                return BytesIO(html)

            def __exit__(self, exc_type, exc, tb):
                return False

        with patch("filtershop_main.admin.urlopen", return_value=DummyResponse()):
            result = EntryOnSteam.get_review_count(DummyAdmin(), None, entry)

        self.assertTrue(result)
        game.refresh_from_db()
        self.assertEqual(game.known_popularity, 21.0)

    def test_get_review_count_updates_entry_name_from_linked_videogame(self):
        entity_type = TypeOfEntity.objects.create(name="Video Game")
        game = Videogame_common.objects.create(name="Synced Game", for_type=entity_type)
        entry = Entry_on_Steam.objects.create(
            appid=54321,
            name="Stale Manual Name",
            videogame=game,
        )

        class DummyAdmin:
            def message_user(self, request, message):
                return None

        html = b'<html><body><span itemprop="reviewCount" content="12"></span></body></html>'

        class DummyResponse:
            def __enter__(self):
                return BytesIO(html)

            def __exit__(self, exc_type, exc, tb):
                return False

        with patch("filtershop_main.admin.urlopen", return_value=DummyResponse()):
            result = EntryOnSteam.get_review_count(DummyAdmin(), None, entry)

        self.assertTrue(result)
        entry.refresh_from_db()
        self.assertEqual(entry.name, "Synced Game")

    def test_get_raw_review_count_stores_value_on_entry(self):
        entry = Entry_on_Steam.objects.create(
            appid=98765,
            name="Raw Count Game",
        )

        class DummyAdmin:
            def message_user(self, request, message):
                return None

        html = b'<html><body><span itemprop="reviewCount" content="77"></span></body></html>'

        class DummyResponse:
            def __enter__(self):
                return BytesIO(html)

            def __exit__(self, exc_type, exc, tb):
                return False

        with patch("filtershop_main.admin.urlopen", return_value=DummyResponse()):
            result = EntryOnSteam.get_raw_review_count(DummyAdmin(), None, entry)

        self.assertTrue(result)
        entry.refresh_from_db()
        self.assertEqual(entry.raw_review_count, 77)
