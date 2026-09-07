from rest_framework import generics, status
from rest_framework.response import Response
from .models import ContactRequest
from .serializers import ContactRequestSerializer

class ContactRequestCreateView(generics.CreateAPIView):
    http_method_names = ['post', 'head', 'options']
    throttle_scope = 'contact'
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "Your message has been submitted successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
