from Register_Login.models import AccessToken, Events, Newsletter,Profile, Receipts, Restaurant_Suggestion, Team_Member, TopCustomers
from django.contrib import admin

# Register your models here.


class Register(admin.ModelAdmin):
    list_filter = ("email","first_name", "last_name", "last_modified")
    list_display = ("email","first_name", 'last_name','last_modified','PhoneNumber','is_active','id'
                  )
    search_fields = ['email']



class Team_Admin(admin.ModelAdmin):
    model = Team_Member
    list_display = ('first_name','last_name','email','PhoneNumber')

class TopCustomers_Admin(admin.ModelAdmin):
    model = Team_Member
    list_display = ('first_name','last_name','email','PhoneNumber')


class Receipts_Admin(admin.ModelAdmin):
    model = Receipts
    list_display = ('created','total_in_cash','order_time','add_by')
    readonly_fields=('add_by',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'add_by', None) is None:
            obj.add_by = request.user
        obj.save()




class Restaurant_Suggestion_Admin(admin.ModelAdmin):
    model = Restaurant_Suggestion
    list_display = ('restaurant_name','email','city','reason')
    list_filter = ('restaurant_name','email','city',)


class AccessTokenAdmin(admin.ModelAdmin):
    model = Profile
    fieldsets = (
        (None, {"fields": (
                'user', 'token', 'expires', 'created'
            )}),
    )
    readonly_fields = ('token','created')
    list_display = ('user', 'token', 'created')

class Event_Admin(admin.ModelAdmin):
    list_display = ('email', "Organization", 'PhoneNumber','date','created')




admin.site.register(Events,Event_Admin)

admin.site.register(Receipts, Receipts_Admin)


admin.site.register(Profile, Register)

admin.site.register(Team_Member, Team_Admin)
admin.site.register(TopCustomers, TopCustomers_Admin)
admin.site.register(Restaurant_Suggestion,Restaurant_Suggestion_Admin)


