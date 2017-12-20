from django.shortcuts import render, redirect
from app.forms import ImageForm
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
        objects = GetImage.objects.all()
        return render(request, 'app/base.html', {'objects': objects})
