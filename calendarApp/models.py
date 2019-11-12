from django.db import models

class Event(models.Model):
    aca = models.ForeignKey(
        'acagiaApp.Academy', related_name='e_aca', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title

