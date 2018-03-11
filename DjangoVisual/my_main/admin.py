from django.contrib import admin
from .models import UserItem_dj,fans_1_Item_dj,fans_2_Item_dj,post_Item_dj,ScrapyItem,test_model

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','screen_name','avatar_hd']
class fans_1Admin(admin.ModelAdmin):
    list_display = ['id','master_id','screen_name','gender']
class fans_2Admin(admin.ModelAdmin):
    list_display = ['id','master_id']
class postAdmin(admin.ModelAdmin):
    list_display = ['id','author_id','created_at','source','retweeted_status']
class scrapyAdmin(admin.ModelAdmin):
    list_display = ['id','task_id']
# Register your models here.
admin.site.register(UserItem_dj,UserAdmin) #定制admin
admin.site.register(fans_1_Item_dj,fans_1Admin)
admin.site.register(fans_2_Item_dj,fans_2Admin)
admin.site.register(post_Item_dj,postAdmin)
admin.site.register(ScrapyItem,scrapyAdmin)
admin.site.register(test_model)