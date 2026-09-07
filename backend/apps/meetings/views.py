from rest_framework import generics, status
from rest_framework.response import Response
from .models import MeetingRequest
from .serializers import MeetingRequestSerializer

class MeetingRequestCreateView(generics.CreateAPIView):
    http_method_names = ['post', 'head', 'options']
    throttle_scope = 'meetings'
    queryset = MeetingRequest.objects.all()
    serializer_class = MeetingRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "Demo request submitted successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
