from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email',''),
            password=validated_data['password']
        )
        return user

class ItemSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'quantity', 'price', 'updated_at', 'created_at', 'created_by')
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by')
    
    def validate_name(self, value):
        """
        check that the item name is unique
        """

        if self.instance is None:
            if Item.objects.filter(name=value).exists():
                raise serializers.ValidationError("An item with this name already exists")
        else:
            if Item.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError('An item with this name already exists.')
        return value