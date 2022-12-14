from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from account.serializers import RegistrationSerializer
from account.models import User


@api_view(['GET', 'POST'])
@permission_classes([])
def registration_view(request):
    """
    this function is used for registering a user into the system.
    :param request:
    :return:
    """
    
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user).key
        response = dict(message='successfully registered.', token=token)
        return Response(response, status=status.HTTP_200_OK)
    else:
        
        response = serializer.errors
        print("Res",response)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def login_view(request):
    """
    this function is used for returning an auth token to a valid user.
    :param request:
    :return:
    """
    print(dir(request))
    print(request.authenticators)
    try:
        user = User.objects.get(username=request.data['username'])
        if user.password != request.data['password']:
            raise Exception
        token, created = Token.objects.get_or_create(user=user)
        response = dict(message='login successful.', token=token.key)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Login Details are incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
