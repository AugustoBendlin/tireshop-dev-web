from random import choices
from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

class Categoria(models.Model):
  modelo = models.CharField(max_length=255)

  def __str__(self):
      return self.modelo

class Fabricante(models.Model):
  nome = models.CharField(max_length=255)
  endereco = models.CharField(max_length=255)

  def __str__(self):
      return self.nome

class Pneu(models.Model):
  codigoFabricacao = models.CharField(max_length=255)
  medida = models.CharField(max_length=255, default="")
  preco = models.FloatField()
  categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="pneus")
  fabricante = models.ForeignKey(Fabricante, on_delete=models.PROTECT, related_name="pneus")

  def __str__(self):
      return "%s (%s)" %(self.fabricante, self.categoria)

class Compra(models.Model):

  class StatusCompra(models.IntegerChoices):
    CARRINHO = 1, 'Carrinho'
    REALIZADO = 2, 'Realizado'
    PAGO = 3, 'Pago'
    ENTREGUE = 4, 'Entregue'

  usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras")
  status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)

  @property
  def total(self):
    queryset = self.itens.all().aggregate(total=models.Sum(F('quantidade') * F('pneu__preco')))
    return queryset["total"]

class ItensCompra(models.Model):
  compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
  pneu = models.ForeignKey(Pneu, on_delete=models.PROTECT, related_name="+")
  quantidade = models.IntegerField()