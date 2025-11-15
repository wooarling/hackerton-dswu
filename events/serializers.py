# events/serializers.py

from rest_framework import serializers
from .models import Event, EventCategory

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'description']

class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer()  # 카테고리 정보를 포함하여 직렬화

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'category', 'location']

    def create(self, validated_data):
        # 카테고리 직렬화된 데이터에서 카테고리 모델을 가져와서 저장
        category_data = validated_data.pop('category')
        category = EventCategory.objects.create(**category_data)
        event = Event.objects.create(category=category, **validated_data)
        return event

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)

        # 이벤트 수정
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.location = validated_data.get('location', instance.location)

        if category_data:
            # 카테고리 수정
            instance.category.name = category_data.get('name', instance.category.name)
            instance.category.description = category_data.get('description', instance.category.description)
            instance.category.save()

        instance.save()
        return instance
