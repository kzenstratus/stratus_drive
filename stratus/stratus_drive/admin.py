from django.contrib import admin

# Register your models here.
from .models import UserProfile

class All_Drives_Admin(admin.ModelAdmin):
	class Meta:
		model = UserProfile
admin.site.register(UserProfile,All_Drives_Admin)