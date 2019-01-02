import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from healthrecords.models import Examination, ExaminationRecord, Test, TestRecord
from accounts.models import User

@receiver(pre_save)
def all_models_validation(instance, *args, **kwargs):
#    instance.full_clean()
    print('all_models_are_validated')

@receiver(post_save, sender=User)
def create_user_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=Examination)
def create_examination_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()


@receiver(post_save, sender=ExaminationRecord)
def create_examination_record_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()

@receiver(post_save, sender=Test)
def create_test_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()


@receiver(post_save, sender=TestRecord)
def create_test_record_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()