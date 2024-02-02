from django.shortcuts import render,HttpResponse, HttpResponseRedirect,redirect,get_object_or_404
from django.views import View
from account.models import User
from django.contrib.auth import authenticate, login, logout
from . decorators import login_required
from django.contrib import messages
from django.contrib import auth
from . forms import *
from app.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from . new_file_handler import validate_file
from django.http import JsonResponse


def login(request):
    try:
        if request.user.is_authenticated:
            return render(request,'app2/index.html')
        if request.method =="POST":
            email = request.POST['useremail']
            print(email)
            password = request.POST['password']
            print(password)
            # user_obj = User.objects.filter(email=email)
            user_obj = authenticate(email=email, password=password)
            print(user_obj)
            if not user_obj: #not user_obj.exists():
                messages.warning(request,"Invalid username and password...")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = authenticate(email=email, password=password)
            if user_obj and user_obj.is_superuser or user_obj.is_editor:
                auth.login(request, user_obj)
                return redirect('dashboard:index')
            messages.warning(request,'Inavlid Password')
            return redirect('dashboard:login')
        return render(request,'app2/login.html')
    except Exception as e:
        print(e)
        messages.warning(request,'something wrong...')
        return redirect('dashboard:login')

@login_required
def userlogout(request):
    auth.logout(request)
    messages.info(request,"logout successfully..")
    return redirect('dashboard:login')


@login_required
def index(request):
    return render(request,'app2/index.html')


@login_required
def aboutUs(request):
    instance = None
    try:
        if id:
            instance = AboutUS.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the AboutUS.')
        return redirect('dashboard:aboutUs')

    if request.method == 'POST':
        form = AboutUSForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'AboutUS edited successfully.')
                return redirect('dashboard:aboutUs')  # Redirect to the edited AboutUS's details page
            else:  # Add operation
                messages.success(request, 'AboutUS added successfully.')
                return redirect('dashboard:aboutUs')  # Redirect to the page for adding new AboutUSs
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = AboutUSForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_about_us.html', context)


#news categorei
@login_required
def add_edit_MainCategorie(request, id=None):
    instance = None
    try:
        if id:
            instance = MainCategorie.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the MainCategorie.')
        return redirect('dashboard:add_MainCategorie')

    if request.method == 'POST':
        form = MainCategorieForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'MainCategorie edited successfully.')
                return redirect('dashboard:edit_MainCategorie', id=instance.id)  # Redirect to the edited MainCategorie's details page
            else:  # Add operation
                messages.success(request, 'MainCategorie added successfully.')
                return redirect('dashboard:add_MainCategorie')  # Redirect to the page for adding new MainCategories
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = MainCategorieForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_MainCategorie.html', context)

@login_required
def mainCategories(request):
    MainCategories=MainCategorie.objects.all()
    p=Paginator(MainCategories,10)
    page_number= request.GET.get('page')
    MainCategories=p.get_page(page_number)
    return render(request, 'app2/MainCategorie.html',{'details':MainCategories})

@login_required
def deleteMainCategorie(request, id):
    record = get_object_or_404(MainCategorie, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:mainCategorie')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/MainCategorie.html', {'details': record})



#news subcategorie
@login_required
def add_edit_SubCategories(request, id=None):
    instance = None
    try:
        if id:
            instance = SubCategorie.objects.get(pk=id)
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the SubCategories.')
        return redirect('dashboard:add_SubCategories')

    if request.method == 'POST':
        form = SubCategorieForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'SubCategories edited successfully.')
                return redirect('dashboard:edit_SubCategories', id=instance.id)  # Redirect to the edited SubCategories's details page
            else:  # Add operation
                messages.success(request, 'SubCategories added successfully.')
                return redirect('dashboard:add_SubCategories')  # Redirect to the page for adding new SubCategoriess
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = SubCategorieForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_SubCategories.html', context)

@login_required
def subCategories(request):
    SubCategories=MainCategorie.objects.all()
    p=Paginator(SubCategories,4)
    page_number= request.GET.get('page')
    SubCategories=p.get_page(page_number)
    return render(request, 'app2/SubCategories.html',{'details':SubCategories})

@login_required
def deleteSubCategories(request, id):
    record = SubCategorie.objects.get(pk=id)
    if request.method == 'POST':
        record.delete()
        messages.success(request,'Sub Categorie Deleted Successfully !')
        return redirect('dashboard:subCategorie')  # Redirect to a list view after deletion
    else:
        return render(request, 'app2/SubCategories.html', {'details': record})



@login_required 
def newsList(request):
    allnews = News.objects.all()
    return render(request,'app2/news_table.html',{'allNews':allnews})


@login_required
def createNews(request):
    allcategorie= MainCategorie.objects.all()
    user= request.user
    if request.method=="POST":
        newstitle = request.POST['title']
        maincategorie= request.POST['categoryselect']
        mainctg = MainCategorie.objects.get(id=maincategorie)
        subcategorie = request.POST['subcategory']
        if subcategorie:
            subctg = SubCategorie.objects.get(id =subcategorie)
        else:
            subctg =None
        # reporter = request.POST['reporter']
        # news_reporter =User.objects.get(id=reporter)
        trending_status=request.POST['trending']
        # short_description = request.POST['shortdiscription']
        news_description = request.POST['description']
        news_image = request.FILES['newsimage']
        new_news= News.objects.create( 
                                      categorie=mainctg,
                                      subCategorie=subctg,
                                      title=newstitle,
                                      discriptions=news_description,
                                      image =news_image,
                                    #   repoter =news_reporter,
                                      trending= trending_status,
                                      
                                      )
        new_news.save()
        messages.success(request,'News added successfully !')
        return redirect('dashboard:createnews')

    else:
        return render(request,'app2/create_news.html',{'allcategorie':allcategorie,
                                                       'user':user
                                                       })
@login_required
def editeNews(request, slug=None):
    news = News.objects.get(news_slug =slug)
    allcategorie= MainCategorie.objects.all()
    user= request.user
    if request.method=="POST":
        news.title = request.POST['title']
        maincategorie= request.POST['categoryselect']
        news.categorie = MainCategorie.objects.get(id=maincategorie)
        subcategorie = request.POST['subcategory']
        if subcategorie:
            news.subCategorie = SubCategorie.objects.get(id =subcategorie)
        else:
            news.subCategorie =None

        news.trending=request.POST['trending']
        news.discriptions = request.POST['description']
        if 'newsimage' in request.FILES:
            news.image = request.FILES['newsimage']
    
        
        news.save()
        messages.success(request,'News updated successfully !')
        return redirect('dashboard:edite_news', slug=news.news_slug)

    
    return render(request,'app2/edite_news.html',{'news':news,
                                                  'allcategorie':allcategorie,
                                                    'user':user
                                                  })

@login_required
def deletenews(request, slug):
    relatedNews= News.objects.get(news_slug=slug)
    relatedNews.delete()
    messages.success(request,"News deleted successfullY !")
    return redirect('dashboard:allnews')

@login_required
def load_sub_category(request):
    main_ctg_id = request.GET.get('programming')
    print(main_ctg_id)
    sub_category = SubCategorie.objects.filter(maincategorie=main_ctg_id)
    return render(request,'app2/listdropdow.html',{'sub_category':sub_category})




# ads sections
@login_required
def add_edit_HorizontalAds(request, id=None):
    instance = None
    try:
        if id:
            instance = HorizontalAds.objects.get(pk=id)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the HorizontalAds.')
        return redirect('dashboard:add_HorizontalAds')

    if request.method == 'POST':
        form = HorizontalAdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'HorizontalAds edited successfully.')
                return redirect('dashboard:edit_HorizontalAds', id=instance.id)  # Redirect to the edited HorizontalAds's details page
            else:  # Add operation
                messages.success(request, 'HorizontalAds added successfully.')
                return redirect('dashboard:add_HorizontalAds')  # Redirect to the page for adding new HorizontalAdss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = HorizontalAdsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_horizontal_ads.html', context)

@login_required
def add_edit_Ads(request, id=None):
    instance = None
    try:
        if id:
            instance = Ads.objects.get(pk=id)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the Ads.')
        return redirect('dashboard:add_Ads')

    if request.method == 'POST':
        form = AdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Ads edited successfully.')
                return redirect('dashboard:edit_Ads', id=instance.id)  # Redirect to the edited Ads's details page
            else:  # Add operation
                messages.success(request, 'Ads added successfully.')
                return redirect('dashboard:add_Ads')  # Redirect to the page for adding new Adss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = AdsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_ads.html', context)

@login_required
def horizontalAds(request):
    horizontalAds=HorizontalAds.objects.all()
    p=Paginator(horizontalAds,10)
    page_number= request.GET.get('page')
    horizontalAds=p.get_page(page_number)
    return render(request, 'app2/horizontalAds.html',{'details':horizontalAds})

@login_required
def deletehorizontalAds(request, id):
    record = get_object_or_404(HorizontalAds, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:horizontalAds')  # Redirect to a list view after deletion

    return render(request, 'app2/horizontalAds.html', {'details': record})


@login_required
def ads(request):
    ads=Ads.objects.all()
    p=Paginator(ads,10)
    page_number= request.GET.get('page')
    ads=p.get_page(page_number)
    return render(request, 'app2/ads.html',{'details':ads})

@login_required
def deleteAds(request, id):
    record = get_object_or_404(Ads, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:ads')  # Redirect to a list view after deletion

    return render(request, 'app2/ads.html', {'details': record})



# ads sections
@login_required
def add_edit_verticleAds(request, id=None):
    instance = None
    try:
        if id:
            instance = VerticleAds.objects.get(pk=id)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the verticleAds.')
        return redirect('dashboard:add_verticleAds')

    if request.method == 'POST':
        form = VerticleAdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'verticleAds edited successfully.')
                return redirect('dashboard:edit_verticleAds', id=instance.id)  # Redirect to the edited verticleAds's details page
            else:  # Add operation
                messages.success(request, 'verticleAds added successfully.')
                return redirect('dashboard:add_verticleAds')  # Redirect to the page for adding new verticleAdss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = VerticleAdsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_verticle_ads.html', context)

@login_required
def verticleAds(request):
    verticleAds=VerticleAds.objects.all()
    p=Paginator(verticleAds,10)
    page_number= request.GET.get('page')
    verticleAds=p.get_page(page_number)
    return render(request, 'app2/verticle_ads.html',{'details':verticleAds})

@login_required
def deleteverticleAds(request, id):
    record = get_object_or_404(HorizontalAds, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:verticleAds')  # Redirect to a list view after deletion

    return render(request, 'app2/verticleAds.html', {'details': record})

@login_required
def popUpAds(request):
    instance = None
    try:
        if id:
            instance = PopUpAds.objects.first()
    except Exception as e:
        messages.warning(request, 'An error occurred while retrieving the AboutUS.')
        return redirect('dashboard:popUpAds')

    if request.method == 'POST':
        form = PopUpAdsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Pop-Up Ads updated successfully.')
                return redirect('dashboard:popUpAds')  # Redirect to the edited popUpAds's details page
            else:  # Add operation
                messages.success(request, 'Pop-Up Ads updated successfully.')
                return redirect('dashboard:popUpAds')  # Redirect to the page for adding new popUpAdss
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = PopUpAdsForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/popupads.html', context)


@login_required
def Contact_Us(request):
    ContactUs_details=ContactUs.objects.all()
    p=Paginator(ContactUs_details,4)
    page_number= request.GET.get('page')
    ContactUs_details=p.get_page(page_number)
    return render(request,'app2/Contact_Us.html',{'details':ContactUs_details})

@login_required
def deleteContactUs(request, id):
    record = get_object_or_404(ContactUs, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:Contact_Us')  # Redirect to a list view after deletion

    return render(request, 'app2/Contact_Us.html', {'details': record})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # update_session_auth_hash(request, user)  # Important to update the session after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard:change_password')  # Redirect to the same view after successful password change
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'app2/change_password.html', {'form': form})





# @login_required
# def about(request):
#     about= AboutUS.objects.first()
#     return render(request,'app2/about.html',{'about':about})

# @login_required
# def update_about(request):
#     if request.method=="POST":
#         id= request.POST['id']
#         about = AboutUS.objects.get(id= id)
#         about.introduction= request.POST['introduction']
#         about.our_story= request.POST['our_story']
#         if 'story_image' in request.FILES:
#             image_file = request.FILES['image1']
#             about.story_image = image_file
#         about.our_values= request.POST['our_values']
#         about.our_mission= request.POST['our_mission']
#         if 'mission_image' in request.FILES:
#             image_file = request.FILES['image2']
#             about.mission_image = image_file
#         about.our_team= request.POST['our_team']

#         about.save()
#         messages.info(request,'Update successfully !')
#         return redirect('dashboard:about')
#     return redirect('dashboard:about')

@login_required
def add_edit_Video(request, id=None):
    instance = None
    try:
        if id:
            instance = Video.objects.get(pk=id)
    except Exception as e:
        print(e)
        messages.warning(request, 'An error occurred while retrieving the Video.')
        return redirect('dashboard:add_Video')

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            if instance:  # Edit operation
                messages.success(request, 'Video edited successfully.')
                return redirect('dashboard:edit_Video', id=instance.id)  # Redirect to the edited Video's details page
            else:  # Add operation
                messages.success(request, 'Video added successfully.')
                return redirect('dashboard:add_Video')  # Redirect to the page for adding new Videos
        else:
            messages.warning(request, 'Form is not valid. Please correct the errors.')
    else:
        form = VideoForm(instance=instance)

    context = {'form': form, 'instance': instance}
    return render(request, 'app2/create_video.html', context)


@login_required
def video(request):
    verticleAds=Video.objects.all()
    p=Paginator(verticleAds,10)
    page_number= request.GET.get('page')
    verticleAds=p.get_page(page_number)
    return render(request, 'app2/video.html',{'details':verticleAds})

@login_required
def deleteVideo(request, id):
    record = get_object_or_404(Video, id=id)

    if request.method == 'POST':
        record.delete()
        return redirect('dashboard:video')  # Redirect to a list view after deletion

    return render(request, 'app2/video.html', {'details': record})