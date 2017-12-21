from django.db import models


class GetImage(models.Model):
    uploaded_by = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='app/static/app/images/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def image_url(self):
        return self.image.url[len('app/static/'):]
