from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
