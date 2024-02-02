from django.db import models
# from .models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
import unidecode
from unidecode import unidecode
from django.template import defaultfilters
from django.contrib.auth.models import User
import nepali_datetime


class AboutUS(models.Model):
    logo= models.ImageField(upload_to='logoimage/')
    title = models.CharField(max_length=1000)
    address = models.CharField(max_length=1000)
    email = models.EmailField()
    website = models.URLField()
    DepartmentRegistrationNo = models.CharField(max_length=150)
    contactNo= models.CharField(max_length=15)
    editor = models.CharField(max_length=200)
    facebookUrl =models.URLField(null=True, blank=True)
    twitterUrl =models.URLField(null=True, blank=True)
    youtubeUrl =models.URLField(null=True, blank=True)
    tiktokUrl = models.URLField(null=True, blank=True)
    locationUrl=models.URLField(null=True, blank=True,max_length=1000)
    class Meta:
        ordering =['-id',]



class PopUpAds(models.Model):
    url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='popads/')

    



class CustomAutoSlugField(AutoSlugField):
    def create_slug(self, model_instance, add):
        slug = super().create_slug(model_instance, add)
        slug = unidecode(slug) 
        return slug
    

class MainCategorie(models.Model):
    categorie_name = models.CharField(max_length=150)
    main_ctg_slug = CustomAutoSlugField(populate_from = 'categorie_name', unique=True, default=None)
    ordering =models.PositiveIntegerField()

    class Meta:
        ordering =['ordering',]

    
    def __str__(self):
        return self.categorie_name
    

class SubCategorie(models.Model):
    maincategorie = models.ForeignKey(MainCategorie, on_delete=models.CASCADE, related_name='categorie')
    subcategorie_name = models.CharField(max_length=150)
    subctgslug= CustomAutoSlugField(populate_from='subcategorie_name', unique=True, default=None)
    ordering =models.PositiveIntegerField()

    class Meta:
        ordering =['ordering',]
    def __str__(self):
        return self.subcategorie_name
    


    
class News(models.Model):
    categorie= models.ForeignKey(MainCategorie, on_delete=models.CASCADE, related_name='mainCtg')
    subCategorie = models.ForeignKey(SubCategorie, on_delete=models.CASCADE, related_name='subCtg', null=True, blank=True)
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='newsimage/')
    discriptions = RichTextField()
    news_slug =CustomAutoSlugField(populate_from='title', unique=True, always_update=True)
    create_date = models.CharField(max_length=50,null=True, blank=True, default=nepali_datetime.date.today().strftime('(%K-%N-%G)'), editable=False)  #max_length=200,default=nepali_datetime.date.today().strftime("%d-%B-%Y")
    update_date = models.DateTimeField(auto_now=True)
    trending= models.BooleanField(default=False)

    class Meta:
        ordering = ['-id',]
        verbose_name = "News"
        verbose_name_plural = "News"

    
   

    def __str__(self):
        return self.title
    



ordering_number =(
    ('first',"First"),
    ('second',"Second"),
    ('third',"Third"),
    ('fourth',"Fourth"),
    ('fifth',"Fifth"),
    ('six',"Six")
)

pages =(
    ('home_page','Home Page'),
    ('news_details','News Detail')
)


class HorizontalAds(models.Model):
    name = models.CharField(max_length=150)
    image =models.ImageField(upload_to='horizontalads/')
    url =models.URLField(null=True, blank=True)
    positionNumber =models.CharField(max_length=150, choices=ordering_number)
    page = models.CharField(max_length=150,choices=pages, default='home_page')
    show = models.BooleanField(default=True)

    class Meta:
        ordering =['-id',]
    

    def __str__(self):
        return self.name


class VerticleAds(models.Model):
    name = models.CharField(max_length=150)
    image =models.ImageField(upload_to='verticleads/')
    url =models.URLField(null=True, blank=True)
    ordering=models.PositiveIntegerField()
    class Meta:
        ordering =['-id',]
    

    def __str__(self):
        return self.name

    
class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    

    class Meta:
        ordering =['-id',]
    
    def __str__(self):
        return self.name
    

class Video(models.Model):
    videoUrl=models.URLField(max_length=1000)
    title=models.CharField(max_length=500)
    

class Ads(models.Model):
    adsImg=models.ImageField(upload_to="ads/")
    title=models.CharField(max_length=500,null=True, blank=True)