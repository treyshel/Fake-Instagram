from django.shortcuts import render, redirect
from app.forms import *
from app.models import GetImage
from django.views import View
from PIL import ImageFilter, Image
from resizeimage import resizeimage


class PhotoView(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'app/post.html', {'form': form})

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            path = 'app/static/' + GetImage.objects.last().image_url()
            image = Image.open(path)
            w, h = image.size
            s = min(w, h)
            image = image.crop(box=(int((w - s) / 2), int((h - s) / 2), int(
                (w + s) / 2), int((h + s) / 2)))
            image = resizeimage.resize_cover(image, [500, 500], validate=False)
            image.save(path)
            return redirect('app:feed')
        else:
            return render(request, 'app/post.html', {'form': form})


class ShowFeed(View):
    def get(self, request):
        objects = GetImage.objects.all().order_by('-uploaded_at')
        return render(request, 'app/feed.html',
                      {'objects': objects,
                       'comment_form': CommentForm()})


class AddFilter(View):
    def get(self, request, image_id):
        form = Filters()
        path = 'app/static/' + GetImage.objects.get(id=image_id).image_url()
        return render(request, 'app/post.html', {'form': form})

    def post(self, request, image_id):
        form = Filters(request.POST)
        path = 'app/static/' + GetImage.objects.get(id=image_id).image_url()
        image = Image.open(path)
        if form.is_valid():
            f = form.filter()
            image.convert('RGB').filter(f).save(path)
            return redirect('app:feed')


class DeletePost(View):
    def post(self, request, image_id):
        GetImage.objects.get(id=image_id).delete()
        return redirect('app:feed')


class AddComment(View):
    def post(self, request, image_id):
        document = GetImage.objects.get(id=image_id)
        form = CommentForm(document, request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:feed')
        else:
            return redirect('app:feed')