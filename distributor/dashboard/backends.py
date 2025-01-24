from django.contrib.auth.backends import ModelBackend
from .models import Distributor

class DistributorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            distributor = Distributor.objects.get(distributor_name=username, distributor_id=password)
        except Distributor.DoesNotExist:
            return None
        if distributor.is_active:
            return distributor
        return None