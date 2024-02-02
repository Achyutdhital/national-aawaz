from . models import*


def mainCategories(request):
    allCategories = MainCategorie.objects.all().order_by('ordering')
    subcategories = SubCategorie.objects.all().order_by('ordering')
    return({
        'allCategories':allCategories,
        'subcategories':subcategories,
        'sidemenu': allCategories,
        'othermenu[10:]':allCategories,
    })


def aboutUs(request):
    about = AboutUS.objects.first()
    return({
        'about':about,
    })

def horizontal_ad(request):
    ad = HorizontalAds.objects.filter(positionNumber='first',page='home_page', show=True).first()
    return({
        'horizontal_ad':ad,
    })


def verticle_ad(request):
    ad = VerticleAds.objects.all()
    return({
        'verticle_ad':ad,
    })

def video(request):
    vd = Video.objects.all()
    return({
        'video':vd,
    })
