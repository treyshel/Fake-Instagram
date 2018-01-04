from django import forms
from app.models import GetImage, Comment
from PIL import ImageFilter


class ImageForm(forms.ModelForm):
    class Meta:
        model = GetImage
        fields = ('uploaded_by', 'image', 'caption', 'topic')


class Filters(forms.Form):
    filter_choices = [('', ''), ('BLUR', 'BLUR'), ('CONTOUR', 'CONTOUR'),
                      ('DETAIL', 'DETAIL'), ('EDGE_ENHANCE', 'EDGE_ENHANCE'),
                      ('EDGE_ENHANCE_MORE', 'EDGE_ENHANCE_MORE'), ('EMBOSS',
                                                                   'EMBOSS'),
                      ('FIND_EDGES', 'FIND_EDGES'), ('SMOOTH', 'SMOOTH'),
                      ('SMOOTH_MORE', 'SMOOTH_MORE'), ('SHARPEN', 'SHARPEN')]

    f = forms.ChoiceField(choices=filter_choices)

    def filter(self):
        return {
            'BLUR': ImageFilter.BLUR,
            'CONTOUR': ImageFilter.CONTOUR,
            'DETAIL': ImageFilter.DETAIL,
            'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE,
            'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
            'EMBOSS': ImageFilter.EMBOSS,
            'FIND_EDGES': ImageFilter.FIND_EDGES,
            'SMOOTH': ImageFilter.SMOOTH,
            'SMOOTH_MORE': ImageFilter.SMOOTH_MORE,
            'SHARPEN': ImageFilter.SHARPEN
        }.get(self.cleaned_data['f'], None)


class CommentForm(forms.Form):
    comment = forms.CharField()

    def __init__(self, document=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.document = document

    def save(self):
        return self.document.comment_set.create(
            comment=self.cleaned_data['comment'])


