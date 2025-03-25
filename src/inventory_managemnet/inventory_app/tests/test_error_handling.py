from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from inventory_app.tests.factories import UserFactory, ItemFactory

class ItemErrorHandlingTest(APITestCase):
    """Test error handling in the API"""
    
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.item = ItemFactory(created_by=self.user)
        self.list_url = reverse("item-list")
        self.detail_url = reverse("item-detail", kwargs={"pk": self.item.pk})
        self.nonexistent_url = reverse("item-detail", kwargs={"pk": 99999})  
    
    def test_get_nonexistent_item(self):
        """Test getting a non-existent item"""
        response = self.client.get(self.nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Item not found")
    
    def test_update_nonexistent_item(self):
        """Test updating a non-existent item"""
        data = {
            "name": "NonexistentItem",
            "description": "This should fail",
            "quantity": 10,
            "price": "99.99",
        }
        response = self.client.put(self.nonexistent_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
    
    def test_delete_nonexistent_item(self):
        """Test deleting a non-existent item"""
        response = self.client.delete(self.nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
    
    def test_invalid_create_data(self):
        """Test creating an item with invalid data"""
        data = {
            "name": "",  # Empty name should be invalid
            "description": "Invalid item",
            "quantity": -5,  # Negative quantity should be invalid
            "price": "abc",  # Invalid price format
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  