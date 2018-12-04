from django.db import models

# Create your models here.



class Member(models.Model):
    #_safedelete_policy = NO_DELETE
    user_uuid = models.UUIDField(db_index=True, unique=True)



