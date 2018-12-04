import uuid
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Other Django Applications


class Snomed(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)

class IcdTen(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)

class IcdNine(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)

class ExaminationStandard(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    snomed = models.ForeignKey(Snomed, related_name='snomed_standard', blank = True , null = True, on_delete=models.PROTECT)
    icd_ten = models.ForeignKey(IcdTen, related_name='icd_ten_standard', blank = True , null = True, on_delete=models.PROTECT)
    icd_nine = models.ForeignKey(IcdNine, related_name='icd_nine_standard', blank = True , null = True, on_delete=models.PROTECT)
    is_snomed = models.BooleanField(default=False)
    is_icd_ten = models.BooleanField(default=False)
    is_icd_nine = models.BooleanField(default=False)
@receiver(post_save, sender=ExaminationStandard)
def create_examination_standard_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()



class Loinc(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)

class Local(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)

class TestStandard(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    loinc = models.ForeignKey(Loinc, related_name='loinc_standard', blank = True , null = True, on_delete=models.PROTECT)
    local = models.ForeignKey(Local, related_name='local_standard', blank = True , null = True, on_delete=models.PROTECT)
    is_loinc = models.BooleanField(default=False)
    is_local = models.BooleanField(default=False)
@receiver(post_save, sender=TestStandard)
def create_test_standard_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()
