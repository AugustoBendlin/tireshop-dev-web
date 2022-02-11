from dataclasses import fields
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from core.models import Categoria, Fabricante, Pneu, Compra, ItensCompra

class CategoriaSerializer(ModelSerializer):
  class Meta:
    model = Categoria
    fields = '__all__'

class FabricanteSerializer(ModelSerializer):
  class Meta:
    model = Fabricante
    fields = '__all__'

class PneuSerializer(ModelSerializer):
  class Meta:
    model = Pneu
    fields = '__all__'

class PneuDetailSerializer(ModelSerializer):
  categoria = CharField(source="categoria.modelo")
  fabricante = FabricanteSerializer()

  class Meta:
    model = Pneu
    fields = "__all__"
    depth = 1

class ItensCompraSerializer(ModelSerializer):
  total = SerializerMethodField()

  class Meta:
    model = ItensCompra
    fields = ("pneu", "quantidade", "total")
    depth = 2

  def get_total(self, instance):
    return instance.quantidade * instance.pneu.preco

class CompraSerializer(ModelSerializer):
  usuario = CharField(source="usuario.email")
  status = SerializerMethodField()
  itens = ItensCompraSerializer(many=True)

  class Meta:
    model = Compra
    fields = ("id", "status", "usuario", "itens", "total")

  def get_status(self, instance):
    return instance.get_status_display()

class CriarEditarItensCompraSerializer(ModelSerializer):
  class Meta:
    model = ItensCompra
    fields = ("pneu", "quantidade")

class CriarEditarCompraSerializer(ModelSerializer):
  itens = CriarEditarItensCompraSerializer(many=True)

  class Meta:
    model = Compra
    fields = ("usuario", "itens")

  def create(self, validated_data):
    itens = validated_data.pop("itens")
    compra = Compra.objects.create(**validated_data)
    for item in itens:
      ItensCompra.objects.create(compra=compra, **item)
    compra.save()
    return compra

  def update(self, instance, validated_data):
    itens = validated_data.pop('itens')
    if itens:
      instance.itens.all().delete()
      for item in itens:
        ItensCompra.objects.create(compra=instance, **item)
      instance.save()
    return instance