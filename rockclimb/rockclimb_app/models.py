from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class rockVideo(models.Model):
    title = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    gym_name = models.CharField(max_length=200, null=True)
    gym_address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    #votes = models.ManyToManyField('Vote', related_name='voted_on')

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rockVideo-detail', kwargs={'pk': self.pk})
    
class Vote(models.Model):
    difficulty = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    rockVideo = models.ForeignKey(rockVideo, related_name='votes', on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=10, null=True)
