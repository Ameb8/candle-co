from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import AdminAccessRequest
from .serializers import AdminAccessRequestSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    # Return whatever fields you want exposed to frontend
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        # Add any other fields you need here
    })

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_staff:
                return Response({'error': 'Admin access only.'}, status=status.HTTP_403_FORBIDDEN)

            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'is_staff': user.is_staff})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterAdminView(APIView):
    permission_classes = [IsAdminUser]  # Only current admins can create new admins

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=400)

        user = User.objects.create_user(username=username, password=password, is_staff=True)
        token = Token.objects.create(user=user)
        return Response({'message': 'Admin created', 'token': token.key})

# Public endpoint: Request admin access
class AdminAccessRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if AdminAccessRequest.objects.filter(user=request.user, approved=None).exists():
            return Response({'error': 'You already have a pending request.'}, status=400)

        reason = request.data.get('reason', '')
        req = AdminAccessRequest.objects.create(user=request.user, reason=reason)
        return Response({'message': 'Admin access request submitted.'}, status=201)

# Admin-only endpoint: View and approve/reject requests
class AdminAccessApprovalView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        requests = AdminAccessRequest.objects.filter(approved=None)
        serializer = AdminAccessRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        req_id = request.data.get('id')
        approve = request.data.get('approve')

        try:
            req = AdminAccessRequest.objects.get(id=req_id, approved=None)
        except AdminAccessRequest.DoesNotExist:
            return Response({'error': 'Request not found or already reviewed.'}, status=404)

        req.approved = bool(approve)
        req.reviewed_by = request.user
        req.reviewed_at = timezone.now()
        req.save()

        if req.approved:
            req.user.is_staff = True
            req.user.save()

        return Response({'message': f"Request {'approved' if req.approved else 'rejected'}."})
