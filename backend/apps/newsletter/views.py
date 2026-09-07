from rest_framework import generics, status
from rest_framework.response import Response
from .models import Subscriber
from .serializers import SubscriberSerializer

class SubscribeView(generics.CreateAPIView):
    http_method_names = ['post', 'head', 'options']
    throttle_scope = 'newsletter'
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Validation failed.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        subscriber, created = Subscriber.objects.get_or_create(email=email)
        if not created:
            if not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save(update_fields=['is_active'])
            return Response({
                "success": True,
                "message": "You are already subscribed to the newsletter.",
                "data": {}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "success": True,
                "message": "Successfully subscribed to the newsletter.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
