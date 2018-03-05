from django.contrib import admin
from .models import Category,Post,Tag,my_model
# Register your models here.



class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','created_time','modified_time','category','author']
class MyAdmin(admin.ModelAdmin):
    list_display = ['id','body','num']
admin.site.register(Post,PostAdmin) #定制admin
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(my_model,MyAdmin)