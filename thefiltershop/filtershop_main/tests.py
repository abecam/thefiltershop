from django.test import TestCase

from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from .models import Entity

class EntityModelTests(TestCase):
    def test_general_rating_not_negative(self):
        """
        general_rating should raise a validation exception if the rating is negative.
        """
        negative_rated_entity = Entity(general_rating=-1)
        try:
            negative_rated_entity.validate_constraints()
        except ValidationError as e:
            self.assertTrue('general_rating' in e.message_dict)
            error = e.message_dict.get('general_rating')
            self.assertEqual('Ensure this value is greater than or equal to 0.', error[0])
            print(e.message_dict)
        
    def test_general_rating_not_above_100(self):
        """
        general_rating should raise a validation exception if the rating is negative.
        """
        negative_rated_entity = Entity(general_rating=101)
        try:
            negative_rated_entity.full_clean()
        except ValidationError as e:
            self.assertTrue('general_rating' in e.message_dict)
            error = e.message_dict.get('general_rating')
            self.assertEqual('Ensure this value is less than or equal to 100.', error[0])


class GaugeTemplateTests(TestCase):
    """Tests to verify gauges render thumbs and accessible attributes."""
    def setUp(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from .models import TypeOfEntity, Videogame_common, Image

        # Minimal required TypeOfEntity
        self.for_type = TypeOfEntity.objects.create(name='Game')

        # Create a videogame entry
        self.game = Videogame_common.objects.create(name='Test Game', for_type=self.for_type, game_type='Indie')

        # Tiny 1x1 PNG
        png_bytes = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
            b'\x00\x00\x00\x0cIDATx\x9cc``\x00\x00\x00\x02\x00\x01\xe2!\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        small_image = SimpleUploadedFile('test.png', png_bytes, content_type='image/png')

        # Attach a title image for the game (used by the view)
        self.title_image = Image.objects.create(title='title', photo=small_image, Entity=self.game)

    def test_gauges_have_thumbs_and_accessibility(self):
        from django.urls import reverse

        url = reverse('filtershop_games:game', args=[self.game.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')

        # Check that both thumb SVG references appear (one per gauge)
        self.assertIn('thumb_up.svg', content)
        self.assertIn('thumb_down.svg', content)

        # Check that aria labels and descriptive alt texts are present for both gauges
        self.assertIn('aria-label="Thumb up for Crapometer"', content)
        self.assertIn('aria-label="Thumb down for Crapometer"', content)
        self.assertIn('aria-label="Thumb up for Hidden Extra Value"', content)
        self.assertIn('aria-label="Thumb down for Hidden Extra Value"', content)

        # Check that each gauge is wrapped in its own .gauge-box with the proper modifier
        self.assertIn('gauge-box--red', content)
        self.assertIn('gauge-box--teal', content)

        # Ensure tooltip titles exist (hover text)
        self.assertIn('title="Thumb up (positive indicator)"', content)
        self.assertIn('title="Thumb down (negative indicator)"', content)