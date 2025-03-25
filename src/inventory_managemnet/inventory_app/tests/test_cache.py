from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.cache import cache
from inventory_app.tests.factories import UserFactory, ItemFactory
from unittest.mock import patch

class ItemCacheTest(APITestCase):
    """Test caching behavior for item details"""
    
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.item = ItemFactory(created_by=self.user)
        self.detail_url = reverse("item-detail", kwargs={"pk": self.item.pk})
        
        # Clear the cache before each test
        cache.clear()
    
    @patch('inventory_app.views.logger')  # Mock the logger to check it's called
    def test_item_cache_hit_miss(self, mock_logger):
        """Test cache hit and miss for item details"""
        # First request - should be a cache miss
        response1 = self.client.get(self.detail_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Check that it logged a cache miss (debug message about database fetch)
        mock_logger.debug.assert_called_with(f"item {self.item.pk} fetched from database and cached")
        mock_logger.reset_mock()
        
        # Second request - should be a cache hit
        response2 = self.client.get(self.detail_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # Check that it logged a cache hit
        mock_logger.debug.assert_called_with(f"Item {self.item.pk} fetched from cache")
    
    def test_cache_invalidation_on_update(self):
        """Test that cache is updated after item update"""
        # First get to cache the item
        self.client.get(self.detail_url)
        
        # Update the item
        data = {
            "name": "CacheUpdateTest",
            "description": "Testing cache invalidation",
            "quantity": 42,
            "price": "42.42",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get again, should return updated data
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data["name"], "CacheUpdateTest")
        self.assertEqual(response.data["quantity"], 42)
    
    def test_cache_invalidation_on_delete(self):
        """Test that cache is invalidated after item deletion"""
        # First get to cache the item
        self.client.get(self.detail_url)
        
        # Delete the item
        self.client.delete(self.detail_url)
        
        # Verify item is gone from database
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)