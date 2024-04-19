from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
def get_default_user():
    # Make sure you have a user with the username 'default_user' or adjust the logic as needed
    user, created = User.objects.get_or_create(username='default_user')
    return user.id

# Create your models here.
class rockVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rock_videos', default=get_default_user)
    title = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    gym_name = models.CharField(max_length=200, null=True)
    gym_address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=False)
    about = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rockVideo-detail', kwargs={'pk': self.pk})
    
class Vote(models.Model):
    difficulty = models.CharField(max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    rockVideo = models.ForeignKey(rockVideo, related_name='votes', on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=10, null=True)
