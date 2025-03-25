from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from inventory_app.tests.factories import UserFactory, ItemFactory

class ItemPaginationTest(APITestCase):
    """Test pagination for items list"""
    
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        
        # Create 15 items for pagination test
        ItemFactory.create_batch(15, created_by=self.user)
        
        self.list_url = reverse("item-list")  
    
    def test_pagination_first_page(self):
        """Test first page of paginated results"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['count'], 15)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 10)  
    
    def test_pagination_second_page(self):
        """Test second page of paginated results"""
        response = self.client.get(f"{self.list_url}?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['count'], 15)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 5)  
    
    def test_pagination_invalid_page(self):
        """Test behavior with invalid page parameter"""
        response = self.client.get(f"{self.list_url}?page=invalid")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should default to page 1
        self.assertEqual(len(response.data['results']), 10)