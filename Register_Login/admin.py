from Register_Login.models import AccessToken, Events, Newsletter,Profile, Receipts, Restaurant_Suggestion, Team_Member, TopCustomers,Push_Notification
from django.contrib import admin
from firebase_admin import messaging

# Register your models here.

tokens = ["f0pi6BPQRy-AK7o8jyN6dH:APA91bHmOSFmhFJPyvLgQ9TkK1ykxtauBQ49Mp5v_-TJ-IkrQZRkeqM_m4ENE1kMrZY2ZMMnED-Sn7RY5vAHnT--u0CyjbHaO_V3HWF8BaGid0R8erzSKgZtM6uhRCjy3-Oh9jjig2j3"]


def sendPush(title,content, registration_token, dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title= title,
            body= content,
            image= 'https://x-eats.com/static/images/logo/logo%20-new.png',
        ),
        data=dataObject,
        tokens= registration_token
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response, message)



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




class pushNotiticationAdmin(admin.ModelAdmin):
    model = Push_Notification
    list_display = ('notification_name','title','content','created','id')

    def save_model(self, request, obj, form, change):
        sendPush(obj.title, obj.content, tokens)
        obj.save()





admin.site.register(Push_Notification, pushNotiticationAdmin)
admin.site.register(Events,Event_Admin)
admin.site.register(Receipts, Receipts_Admin)
admin.site.register(Profile, Register)
admin.site.register(Team_Member, Team_Admin)
admin.site.register(TopCustomers, TopCustomers_Admin)
admin.site.register(Restaurant_Suggestion,Restaurant_Suggestion_Admin)


