from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Topic(models.Model):
    name = models.CharField(max_length=8)

    def __str__(self):
        return self.name


class GetImage(models.Model):
    uploaded_by = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='app/static/app/images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, blank=True, null=True)

    def image_url(self):
        return self.image.url[len('app/static/'):]


class Comment(models.Model):
    comment = models.CharField(max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(GetImage, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
