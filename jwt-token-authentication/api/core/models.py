from django.db import models


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_date = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_date = models.DateTimeField(auto_now=True)

    created_uid = models.ForeignKey('User', related_name='user5', blank=True, null=True)
    updated_uid = models.ForeignKey('User', related_name='user6', blank=True, null=True)

    class Meta:
        abstract = True

        # By default, any model that inherits from `TimestampedModel` should
        # be ordered in reverse-chronological order. We can override this on a
        # per-model basis as needed, but reverse-chronological is a good
        # default ordering for most models.
        ordering = ['-created_date', '-updated_date']
