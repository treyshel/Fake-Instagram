from django.shortcuts import render, redirect
from app.forms import *
from app.models import GetImage
from django.views import View


class PhotoView(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'app/post.html', {'form': form})

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app:feed')
        else:
            return render(request, 'app/post.html', {'form': form})


class ShowFeed(View):
    def get(self, request):
        objects = GetImage.objects.all().order_by('-uploaded_at')
        return render(request, 'app/feed.html', {'objects': objects})


# class AddFilter(View):
#     def get(self, request, image_id):
#         form = Filters()
#         path = 'app/static/' + models.GetImage.objects.get(
#             id=image_id).image_url()
#         return render(request, 'app/post.html', {'form': form})

#     def post(self, request, image_id):


class DeletePost(View):
    def post(self, request, image_id):
        GetImage.objects.get(id=image_id).delete()
        return redirect('app:feed')