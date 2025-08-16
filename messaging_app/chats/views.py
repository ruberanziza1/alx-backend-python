from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import CustomPagination
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.decorators import action


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Get participants from request data (expects list of user_ids)
        participant_ids = request.data.get("participants", [])
        if not participant_ids or len(participant_ids) < 2:
            return Response({"error": "At least two participants are required."}, status=400)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() < 2:
            return Response({"error": "Invalid participant user IDs."}, status=400)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        if not all([sender_id, conversation_id, message_body]):
            return Response({"error": "sender_id, conversation_id, and message_body are required."}, status=400)

        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except (User.DoesNotExist, Conversation.DoesNotExist):
            return Response({"error": "Invalid sender or conversation ID."}, status=404)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        # Only show messages for conversations the user is a participant in
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if self.request.user in conversation.participants.all():
                    return Message.objects.filter(conversation=conversation)
                else:
                    return Message.objects.none()
            except Conversation.DoesNotExist:
                return Message.objects.none()
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)
