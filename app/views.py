from django.shortcuts import render, redirect
from app.forms import *
from app.models import GetImage
from django.views import View
from PIL import ImageFilter, Image
from resizeimage import resizeimage
from django.contrib.auth import login, authenticate


class PhotoView(View):
    def post(self, request):
        user = request.user
        form = ImageForm(user.profile, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            path = 'app/static/' + GetImage.objects.last().image_url()
            image = Image.open(path)
            w, h = image.size
            s = min(w, h)
            image = image.crop(
                box=(int((w - s) / 2), int((h - s) / 2), int((w + s) / 2),
                     int((h + s) / 2)))
            image = resizeimage.resize_cover(image, [500, 500], validate=False)
            image.save(path)
            return redirect('app:feed')
        else:
            return render(request, 'app/post.html', {'form': form})

    def get(self, request):
        form = ImageForm()
        return render(request, 'app/post.html', {'form': form})


class ShowFeed(View):
    def get(self, request):
        objects = GetImage.objects.all().order_by('-uploaded_at')
        return render(request, 'app/feed.html', {
            'objects': objects,
            'comment_form': CommentForm()
        })


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


class Like(View):
    def post(self, request, image_id):
        add_like = GetImage.objects.get(id=image_id)
        add_like.likes += 1
        add_like.save()
        return redirect('app:feed')


class MostPopular(View):
    def get(self, request):
        objects = GetImage.objects.all().order_by('-likes')[:5]
        return render(request, 'app/most-likes.html', {'objects': objects})


class GetTopic(View):
    def get(self, request, topic_id):
        objects = GetImage.objects.filter(topic_id=topic_id)
        return render(request, 'app/feed.html', {'objects': objects})


class BuzzingComments(View):
    def get(self, request):
        objects = sorted(
            GetImage.objects.all(),
            key=lambda obj: obj.comment_set.count())[::-1]
        return render(request, 'app/buzzing-comments.html', {
            'objects': objects
        })


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'app/sign-up.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db(
            )  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('app:feed')
        else:
            form = SignUpForm()
            return render(request, 'app/sign-up.html', {'form': form})


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('app:feed')
        else:
            form = LoginForm()
            return render(request, 'app/login.html', {'form': form})
