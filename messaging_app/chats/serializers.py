# chats/serializers.py
from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault()) # Example: current user as sender
    # OR: If you want to display sender's username
    # sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']
        read_only_fields = ['timestamp'] # Timestamp is auto_now_add

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True) # For displaying messages within a chat
    # If you want to write messages along with chat creation/update, you'd need to
    # override create/update methods or use a package like drf-writable-nested.
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # OR: If you want to display participant usernames
    # participants = serializers.StringRelatedField(many=True, read_only=True)


    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    # Example of how to handle nested writable messages if you choose to implement
    # custom create/update. This is often more complex than using a dedicated package.
    # For a simpler approach, consider 'drf-writable-nested'.
    def create(self, validated_data):
        # This example assumes messages are passed as a list of dicts in 'messages' field
        # and you want to create them along with the chat.
        messages_data = validated_data.pop('messages', [])
        chat = Chat.objects.create(**validated_data)
        for message_data in messages_data:
            Message.objects.create(chat=chat, **message_data)
        return chat

    def update(self, instance, validated_data):
        # Similar logic for updating messages
        messages_data = validated_data.pop('messages', None)
        instance.participants.set(validated_data.get('participants', instance.participants.all()))
        instance.save()

        if messages_data is not None:
            # Here you would typically compare existing messages and update/create/delete them
            # This can get complicated quickly. For simple cases, you might just append new messages.
            # For robust handling, especially updates/deletions of nested items,
            # drf-writable-nested is highly recommended.
            pass # Implement your update logic for messages here

        return instance
