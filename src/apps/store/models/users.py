from common.abstract_models import BaseModelClass
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class UserClient(BaseModelClass):
    name = models.CharField(verbose_name="Name: ", max_length=50)
    code = models.IntegerField(verbose_name="Code: ")

    def __str__(self):
        return self.name


@receiver(pre_save, sender=UserClient)
def signal_pre_save_contract(sender, instance, **kwargs):
    query_for_ger_user_client = UserClient.objects.filter(pk=instance.pk)
    if not query_for_ger_user_client.exists():
        try:
            user_client_with_code_bigger = UserClient.objects.latest("code")
        except UserClient.DoesNotExist:
            user_client_with_code_bigger = None
        if user_client_with_code_bigger is None:
            instance.code = 10000
        else:
            last_code = user_client_with_code_bigger.code
            instance.code = last_code + 1
