from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
    
    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data
    
    def validate_custom_field(self, value):
        # Replace 'some_condition' with your actual validation logic
        if len(value) < 5:  # Example condition
            raise serializers.ValidationError("Custom validation message")
        return value

# Example of using CharField if needed
class CustomMessageSerializer(serializers.ModelSerializer):
    custom_field = serializers.CharField(max_length=200, required=False)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'custom_field']
