from django.contrib import admin
from . models import *





admin.site.register(PopUpAds)

class AboutUSAdmin(admin.ModelAdmin):
    model = AboutUS
    list_display =['id','logo','title','DepartmentRegistrationNo' ,'editor','contactNo','email' , 'address'  , 'website','facebookUrl','twitterUrl','youtubeUrl','tiktokUrl','locationUrl']
    
    fieldsets = (
      ('About Us', {
          'fields': ('logo','title','DepartmentRegistrationNo' ,'editor')
      }),
      ('Contact Details', {
          'fields': ('contactNo','email' , 'address'  , 'website',)
      }),
      ('Social Media', {
          'fields': ('facebookUrl','twitterUrl','youtubeUrl','tiktokUrl','locationUrl' )
      })
   )
    
    def has_add_permission(self, request, obj=None):
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
    
admin.site.register(AboutUS,AboutUSAdmin)





    

class SubcategorieAdmin(admin.TabularInline):
    model =SubCategorie

class MainCategorieAdmin(admin.ModelAdmin):
    inlines =[SubcategorieAdmin]
    list_display = ['categorie_name','ordering']
admin.site.register(MainCategorie, MainCategorieAdmin)




class NewsAdmin(admin.ModelAdmin):
    model = News
    list_display =['id','title','trending','create_date']
    list_filter=['trending']
    list_editable = ['trending']
    list_per_page= 10
    
admin.site.register(News, NewsAdmin)



# class ContactUsAdmin(admin.ModelAdmin):
#     model = ContactUs
#     list_display = ['name','email']
#     list_editable = ['email']

#     def has_add_permission(self, request, obj=None):
#         return False
    
#     def has_delete_permission(self, request, obj=None):
#         return False
    
#     def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
#         context.update({
#             'show_save': True,
#             'show_save_and_continue': False,
#             'show_save_and_add_another': False,
#             'show_delete': False
#         })
#         return super().render_change_form(request, context, add, change, form_url, obj)
    
# admin.site.register(ContactUs, ContactUsAdmin)




class ContactUsAdmin(admin.ModelAdmin):
    model = ContactUs
    list_display =['id','name','email','subject','message']
    list_per_page= 10
    
admin.site.register(ContactUs, ContactUsAdmin)

class HorizontalAdsAdmin(admin.ModelAdmin):
    model = HorizontalAds
    list_display =['id','name','image','url','positionNumber','page','show']
    list_per_page= 10
    
admin.site.register(HorizontalAds, HorizontalAdsAdmin)



class VerticleAdsAdmin(admin.ModelAdmin):
    model = VerticleAds
    list_display =['id','name','image','url','ordering']
    list_per_page= 10
    
admin.site.register(VerticleAds, VerticleAdsAdmin)

class VideoAdmin(admin.ModelAdmin):
    model = Video
    list_display =['id','videoUrl','title']
    list_per_page= 10
    
admin.site.register(Video, VideoAdmin)

class AdsAdmin(admin.ModelAdmin):
    model = Ads
    list_display =['id','adsImg','title']
    list_per_page= 10
    
admin.site.register(Ads, AdsAdmin)