from django import forms
from app.models import *
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MainCategorieForm(forms.ModelForm):
    class Meta:
        model = MainCategorie
        fields = '__all__'

class SubCategorieForm(forms.ModelForm):
    class Meta:
        model = SubCategorie
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

class HorizontalAdsForm(forms.ModelForm):
    class Meta:
        model = HorizontalAds
        fields = '__all__'

class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = '__all__'
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'

class HorizontalAdsForm(forms.ModelForm):
    class Meta:
        model = HorizontalAds
        fields = '__all__'

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        
class AboutUSForm(forms.ModelForm):
    class Meta:
        model = AboutUS
        fields = '__all__'


class PopUpAdsForm(forms.ModelForm):
    class Meta:
        model = PopUpAds
        fields ='__all__'

class VerticleAdsForm(forms.ModelForm):
    class Meta:
        model = VerticleAds
        fields ='__all__'
