from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def cloudmosaic_exception_handler(exc, context):
    """
    Custom exception handler to coerce all API errors into the CloudMosaic contract:
    {
      "success": False,
      "message": "...",
      "errors": {}
    }
    """
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # If the request doesn't start with /api/, fall back to standard Django/DRF behavior
    request = context.get('request')
    if request and not request.path.startswith('/api/'):
        return response

    if response is not None:
        # It's a standard DRF exception (400, 401, 403, 404, 405, 429, etc)
        # We need to map it to our format.
        
        custom_response_data = {
            "success": False,
            "message": "An error occurred.",
            "errors": {}
        }
        
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data["message"] = "Validation failed."
            # The errors might already be nested appropriately or just a flat dict/list
            if isinstance(response.data, dict):
                # If there's a 'success' key, it means the view itself might have already formatted it (our views currently do not do this manually, but just in case)
                if 'success' in response.data:
                    return response
                custom_response_data["errors"] = response.data
            else:
                custom_response_data["errors"] = {"detail": response.data}
                
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data["message"] = "Authentication required."
            
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data["message"] = "Permission denied."
            
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data["message"] = "Not found."
            
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            custom_response_data["message"] = f"Method '{request.method}' not allowed."
            
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            custom_response_data["message"] = "Too many requests. Please try again later."
            
        else:
            # Fallback for any other DRF exception
            if isinstance(response.data, dict) and 'detail' in response.data:
                custom_response_data["message"] = response.data['detail']

        response.data = custom_response_data

    else:
        # Unhandled 500 server error
        logger.error(f"Unhandled Exception in API: {exc}", exc_info=True)
        return Response({
            "success": False,
            "message": "Internal server error.",
            "errors": {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
