from django.db import models


class GetImage(models.Model):
    uploaded_by = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='app/static/app/images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def image_url(self):
        return self.image.url[len('app/static/'):]


class Comment(models.Model):
    comment = models.CharField(max_length=120)
    time = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(GetImage, on_delete=models.CASCADE)
