from rest_framework.generics import ListAPIView
from .serializers import AreaSerializer
from .models import Area


class AreasViews(ListAPIView):
    serializer_class = AreaSerializer
    queryset = Area.objects.all()
