from accounts.serializers.admin_serializer import AdminSerializer as AS
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, authentication_classes, \
    parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated


class CustomAuthToken(ObtainAuthToken):
    # @api_view(['POST'])
    # @authentication_classes((TokenAuthentication,))
    # @permission_classes((IsAuthenticated,))
    # @csrf_exempt    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.uuid_user.user_uuid.hex,
            'email': user.email
        })

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def Logout(request):
    if request.user.is_authenticated == False:
        return HttpResponse('already loggedout')
    else:
        #logout(request)
        user = User.objects.get(username = request.user)
        Token.objects.filter(user=user).delete()
        token, created = Token.objects.get_or_create(user=user)

        #context = { REDIRECT_FIELD_NAME: request.GET.get(REDIRECT_FIELD_NAME, '/')}
        return JsonResponse({
            'token': token.key,
            'user_id': user.uuid_user.user_uuid.hex,
            'email': user.email
        })

# @parser_classes((JSONParser,))
def test2(request, format=None):
    print(request.POST)
    serializer = AS(data = request.POST)

    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()

    return JsonResponse({'received data': request.POST}, safe=False, status=200)
    