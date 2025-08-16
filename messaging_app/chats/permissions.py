from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only authenticated users who are participants of the conversation can access or modify it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj is either a Message or Conversation
        conversation = getattr(obj, 'conversation', obj)
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user in conversation.participants.all()
        return False
