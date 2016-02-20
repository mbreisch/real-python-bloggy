from django.contrib import admin
from models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','views')

# Register your models here.
admin.site.register(Post,PostAdmin)


