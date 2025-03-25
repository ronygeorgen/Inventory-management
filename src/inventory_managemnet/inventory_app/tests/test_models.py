from django.test import TestCase
from inventory_app.tests.factories import UserFactory, ItemFactory  
from inventory_app.models import Item

class ItemModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.item = ItemFactory(created_by=self.user)

    def test_item_creation(self):
        """Test if Item is created successfully"""
        self.assertIsNotNone(self.item.pk)  
        self.assertEqual(self.item.created_by.username, self.user.username)

    def test_item_string_representation(self):
        """Test string representation of the item"""
        self.assertEqual(str(self.item), self.item.name)
        
    def test_item_fields(self):
        """Test item field values"""
        self.assertTrue(isinstance(self.item.name, str))
        self.assertTrue(isinstance(self.item.description, str))
        self.assertTrue(isinstance(self.item.quantity, int))
        self.assertGreaterEqual(self.item.quantity, 0)