from django.contrib import admin
from myapp.models import Student, Article, Publication, Place, Reporter, Restaurant

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "email") #Những cột sẽ hiển thị trên trang admin

admin.site.register(Student, StudentAdmin)
admin.site.register(Place)
admin.site.register(Restaurant)