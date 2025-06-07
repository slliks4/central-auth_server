# Models Import
from ..models import CustomUser

# Serializers Import
from ..serializers.user import UserSerializer

# RestFrameWork (DRF) Import
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Utils Import
# from system_auth.utils.lifecycle import on_create, on_delete, on_update
from system_auth.utils.authenticate_password import is_password_authentic
from core.utils.email import is_email_valid
from core.utils.helper import mask_email, mask_phone

# User Creation Logic
@api_view(['POST'])
def create_user(request) -> Response:
    try:
        # 1. Extract data with safe defaults
        email = request.data.get('email', '').strip().lower()
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')
        skip_name_check = request.data.get('skip_name_check')

        # 2. Email validation
        if not is_email_valid(email):
            return Response({
                'status': 'error',
                'message': 'Invalid email address.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 3. Password validation
        is_valid, error_msg = is_password_authentic(password, confirm_password)
        if not is_valid:
            return Response({
                'status': 'error',
                'message': error_msg
            }, status=status.HTTP_400_BAD_REQUEST)

        # 4. Duplication checks
        if CustomUser.objects.filter(email=email).exists():
            return Response({
                'status': 'error',
                'message': 'Email already registered.'
            }, status=status.HTTP_409_CONFLICT)

        if not skip_name_check:
            matching_users = CustomUser.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )
            if matching_users.exists():
                user = matching_users.first()
                return Response({
                    'status': 'error',
                    'message': 'User with same name exists.',
                    'reason': 'possible_duplicate_name',
                    'suggested_recovery': {
                        'masked_email': mask_email(user.email),
                        'last4_phone': mask_phone(user.phone) if user.phone else None
                    }
                }, status=status.HTTP_409_CONFLICT)

        # 5. Create user
        try:
            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Account creation failed: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 6. Serialize and trigger post-create lifecycle hooks
        try:
            serialized_user = UserSerializer(user, many=False)

            # send_verification_email`(user)
            # Optional lifecycle hooks (e.g., audit logs, email)
            # on_create(serialized_user.data)

            return Response({
                'status': 'success',
                'data': serialized_user.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Serialization failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_user(request) -> Response:
    return request

@api_view(['DELETE'])
def delete_user(request) -> Response:
    return request