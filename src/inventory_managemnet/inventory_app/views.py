import logging
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import UserSerializer, ItemSerializer
from rest_framework.response import Response
from .models import Item
from django.core.cache import cache
from django.http import Http404


logger =  logging.getLogger('inventory_app')

class RegisterView(APIView):
    permission_classes = [ permissions.AllowAny ]

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        try:
            logger.info(f"User registration attempt: {request.data.get('username')}")
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"User registration failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ItemListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = Item.objects.all()

        page = request.query_params.get('page',1)
        try:
            page = int(page)
        except ValueError:
            page = 1
        
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        paginated_items = items[start:end]
        serializer = ItemSerializer(paginated_items, many=True)

        total_items = items.count()
        total_pages = (total_items + page_size - 1) // page_size

        logger.info(f"Retrieved item list, page {page} of {total_pages}")

        return Response({
            'count': total_items,
            'next': f"/api/items/?page={page+1}" if page < total_pages else None,
            'previous': f"/api/items/?page={page-1}" if page > 1 else None,
            'results': serializer.data
        })
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        try:
            if serializer.is_valid():
                logger.info(f"Creating new item: {serializer.validated_data.get('name')}")
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid item data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Item creation failed: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class ItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        cache_key = f'item_{pk}'
        item = cache.get(cache_key)

        if item is None:
            try:
                item = Item.objects.get(pk=pk)
                cache.set(cache_key, item, timeout=60*15)
                logger.debug(f"item {pk} fetched from database and cached")
            except Item.DoesNotExist:
                logger.warning(f"Item {pk} not found")
                raise Http404("Item not found")
        else:
            logger.debug(f"Item {pk} fetched from cache")
        return item
    
    def get(self, request, pk):
        try:
            item = self.get_object(pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Http404:
            return Response({"detail": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            item = self.get_object(pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                logger.info(f"Updating item {pk}")
                serializer.save()

                #update cache with new data
                cache_key = f"item_{pk}"
                cache.set(cache_key, serializer.instance, timeout=60*15)
                return Response(serializer.data)
        except Http404:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            item = self.get_object(pk)
            item_id = item.id
            item.delete()
            
            #delete from cache
            cache_key = f"item_{item_id}"
            cache.delete(cache_key)

            logger.info(f"Deleted item {item_id}")
            return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)