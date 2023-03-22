from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Author, Publication, Comment
from .serializers import AuthorSerializer, PublicationSerializer, CommentSerializer
from .permissions import PermissionPolicyMixin,  PermissionAdminOrOwner


class PublicationViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [AllowAny],
        'update': [PermissionAdminOrOwner],
        'destroy': [PermissionAdminOrOwner],
        'retrieve': [AllowAny]
    }


##############################  AUTHORS  ##############################

class AuthorViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes_per_method = {
        'list': [IsAuthenticated, IsAdminUser],
        'create': [AllowAny],
        'update': [PermissionAdminOrOwner],
        'destroy': [IsAdminUser],
        'retrieve': [IsAdminUser, IsAuthenticated]
    }


##############################  COMMENTS  ##############################

class CommentViewSet(PermissionPolicyMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_per_method = {
        'list': [AllowAny],
        'create': [AllowAny],
        'update': [PermissionAdminOrOwner],
        'destroy': [PermissionAdminOrOwner],
        'retrieve': [AllowAny]
    }

