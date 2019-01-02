from django.db import models


class Member(models.Model):
    #_safedelete_policy = NO_DELETE
    user_uuid = models.UUIDField(db_index=True, unique=True)

    @property
    def popularity(self):
        likes = 12
        time = 12 #hours since created
        return likes / time if time > 0 else likes

    def clean(self):
        print('Member is Cleaned.')
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        print('Member is clean_fielded.')




