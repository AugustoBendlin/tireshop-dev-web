from cgitb import lookup
from unicodedata import name
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from core.models import Categoria
from core.models import Fabricante

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

import json

def teste(request):
  return HttpResponse("Olá mundo")

@method_decorator(csrf_exempt, name="dispatch")
class CategoriaView(View):
  def get(self, request, id=None):
    if id:
      qs = Categoria.objects.get(id=id)
      data = {}
      data['id'] = qs.id
      data['modelo'] = qs.modelo
      return JsonResponse(data)
    else:
      data = list(Categoria.objects.values())
      formatted_data = json.dumps(data, ensure_ascii=False)
      return HttpResponse(formatted_data, content_type="application/json")

  def post(self, request):
    json_data = json.loads(request.body)
    nova_categoria = Categoria.objects.create(**json_data)
    data = {"id": nova_categoria.id, "modelo": nova_categoria.modelo}
    return JsonResponse(data)

  def patch(self, request, id):
    json_data = json.loads(request.body)
    qs = Categoria.objects.get(id=id)
    qs.modelo = json_data['modelo'] #if 'modelo' in json_data else qs.modelo
    qs.save()
    data = {}
    data['id'] = qs.id
    data['modelo'] = qs.modelo
    return JsonResponse(data)

  def delete(self, request, id):
    qs = Categoria.objects.get(id=id)
    qs.delete()
    data = {"mensagem": "Item excluído com sucesso."}
    return JsonResponse(data)

class CategoriaSerializer(ModelSerializer):
  class Meta:
    model = Categoria
    fields = '__all__'

class FabricanteSerializer(ModelSerializer):
  class Meta:
    model = Fabricante
    fields = '__all__'

class CategoriasList(APIView):
  def get(self, request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)

  def post(self, request):
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoriaDetail(APIView):
  def get(self, request, id):
    categoria = get_object_or_404(Categoria.objects.all(), id=id)
    serializer = CategoriaSerializer(categoria)
    return Response(serializer.data)

  def put(self, request, id):
    categoria = get_object_or_404(Categoria.objects.all(), id=id)
    serializer = CategoriaSerializer(categoria, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id):
    categoria = get_object_or_404(Categoria.objects.all(), id=id)
    categoria.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class CategoriaListGeneric(ListCreateAPIView):
  queryset = Categoria.objects.all()
  serializer_class = CategoriaSerializer

class CategoriaDetailGeneric(RetrieveUpdateDestroyAPIView):
  lookup_field = 'id'
  queryset = Categoria.objects.all()
  serializer_class = CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
  queryset = Categoria.objects.all()
  serializer_class = CategoriaSerializer

class FabricanteViewSet(ModelViewSet):
  queryset = Fabricante.objects.all()
  serializer_class = FabricanteSerializer
