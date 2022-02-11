from rest_framework.viewsets import ModelViewSet

from core.models import Pneu
from core.serializers import PneuSerializer, PneuDetailSerializer

class PneuViewSet(ModelViewSet):
  queryset = Pneu.objects.all()
  # serializer_class = PneuSerializer
  def get_serializer_class(self):
    if self.action == "list":
      return PneuDetailSerializer
    if self.action == "retrieve":
      return PneuDetailSerializer
    return PneuSerializer