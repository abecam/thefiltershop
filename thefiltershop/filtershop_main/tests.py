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