from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django_extensions.db.fields import json
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import io
from .models import Member
from .serializers import ServiceaccountMemberSerializer as SMS


def test(request):
    members  = Member.objects.all()
    print(members)
    # serializer = SMS(members, context={'allowed_fields': ('id,_excluder')}, many = True)
    serializer = SMS(members, fields=('id', 'hello', 'exclud', 'popularity'), many = True)
    # serfields = SMS.get_field()
    json = JSONRenderer().render(serializer.data)
    print(json)
    return HttpResponse('In serviceaccounts/views/test. and members serialized data is : ' + 'json')

@parser_classes((JSONParser,))
def test2(request, format=None):
    # stream = io.BytesIO(request.body)
    # data = JSONParser().parse(stream)
    # print(request.body)
    # data2 = {"user_uuid": 'a52b9c20-1279-4a97-b060-5a829a8b00e2', 'popularity': 1}
    # serializer = SMS(data = eval(data))
    print(request.POST)
    serializer = SMS(data = request.POST)

    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()

    return JsonResponse({'received data': request.POST}, safe=False, status=200)
    # return JsonResponse({'received data': json.dumps(list(request.body))}, safe=False, status=200)
    # return HttpResponse('In serviceaccounts/views/test. and members serialized data is : ' + 'json')