# RestFrameWork (DRF) Import
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models Import
from ..models import CustomUser

# Utils Import
from system_auth.utils.authenticate_password import is_password_authentic
from core.utils.email import is_email_valid
from core.utils.helper import mask_email, mask_phone

# Views
@api_view(['POST'])
def create_user(request) -> Response:
    try:
        # Get Request Data
        email =  request.data.get('email', '').lower().strip()
        first_name = request.data.get('first_name', '').strip()
        last_name = request.data.get('last_name', '').strip()
        password = request.data.get('password', '')
        confirm_password = request.data.get('confirm_password', '')
        skip_name_check = request.data.get('skip_name_check', '').lower() == 'true'

        # Verify Email
        if not is_email_valid(email):
            return Response({'error': 'Invalid Email address.'}, status=400)
        
        # Verify Password
        is_valid, error_msg = is_password_authentic(password, confirm_password)
        if not is_valid:
            return  Response({'error': error_msg}, status=400)

        # Check for account Duplication
        ## Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=409)
        ## Soft check on first+last name unless explicitly skipped
        if not skip_name_check:
            matching_users = CustomUser.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )

            if matching_users.exists():
                user = matching_users.first()
                return Response({
                    "warning": "User with same name exists.",
                    "suggested_recovery": {
                        "masked_email": mask_email(user.email),
                        "last4_phone": mask_phone(user.phone) if user.phone else None
                    },
                    "reason": "possible_duplicate_name"
                }, status=409)

# TODO: Finish up the creation of user and set up email backend for verification. Tidy up on_create and other lifecycle function for now
        # Create User account
        # user = CustomUser.objects.create_user(
        #     email=email,
        #     first_name=first_name,
        #     last_name=last_name,
        #     password=password,
        # )
        #
        # serialized_user = UserSerializer(user, many=False)
        # on_create(serializer_class.data)
        return Response({'success': 'it worked'}, status=201)

    except ValueError as e:
        return Response({'error': str(e)}, status=400)


@api_view(['PUT'])
def update_user(request) -> Response:
    return request

@api_view(['DELETE'])
def delete_user(request) -> Response:
    return request