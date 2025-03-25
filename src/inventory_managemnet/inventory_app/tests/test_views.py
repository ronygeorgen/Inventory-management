from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from inventory_app.tests.factories import UserFactory, ItemFactory  
from inventory_app.models import Item

class ItemAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.item = ItemFactory(created_by=self.user)
        self.list_url = reverse("item-list")  
        self.detail_url = reverse("item-detail", kwargs={"pk": self.item.pk})  

    def test_get_items_list(self):
        """Test retrieving list of items"""
        # Create 2 more items
        ItemFactory.create_batch(2, created_by=self.user)
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  
        # Test pagination structure
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 3)

    def test_get_item(self):
        """Test retrieving a single item"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.item.name)

    def test_create_item(self):
        """Test creating an item"""
        data = {
            "name": "NewItem",
            "description": "A test item",
            "quantity": 10,
            "price": "99.99",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)  
        
        # Verify created item data
        self.assertEqual(response.data["name"], "NewItem")
        self.assertEqual(response.data["quantity"], 10)

    def test_update_item(self):
        """Test updating an item"""
        data = {
            "name": "UpdatedItem",
            "description": "Updated description",
            "quantity": 50,
            "price": "199.99",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "UpdatedItem")
        
        # Verify in database
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "UpdatedItem")
        self.assertEqual(self.item.quantity, 50)

    def test_delete_item(self):
        """Test deleting an item"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(Item.objects.count(), 0)
        self.assertIn("message", response.data)  

class UnauthenticatedItemAPITest(APITestCase):
    """Test API access for unauthenticated users"""
    
    def setUp(self):
        self.user = UserFactory()
        self.item = ItemFactory(created_by=self.user)
        self.list_url = reverse("item-list")  
        self.detail_url = reverse("item-detail", kwargs={"pk": self.item.pk})  
    
    def test_get_items_unauthenticated(self):
        """Test that unauthenticated users cannot access items list"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_item_unauthenticated(self):
        """Test that unauthenticated users cannot create items"""
        data = {
            "name": "Unauthorized Item",
            "description": "This should fail",
            "quantity": 5,
            "price": "50.00",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)