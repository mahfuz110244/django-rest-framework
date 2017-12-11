from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False)

class ContactUser(models.Model):
    username = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=True)
    contact_id = models.ForeignKey(Contact, related_name="contacts")

class Attendee(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True,related_name="contacts1")
    attribute_key = models.CharField(max_length=50, blank=True, null=True)
    attribute_value = models.TextField(max_length=500, blank=True, null=True)
    class Meta:
        unique_together = (("contact_id", "attribute_key"),)