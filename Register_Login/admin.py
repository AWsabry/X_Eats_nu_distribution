from Register_Login.models import AccessToken, Events, Newsletter, Notification_token,Profile, Receipts, Restaurant_Suggestion, Team_Member, TopCustomers,Push_Notification
from django.contrib import admin
from firebase_admin import messaging

# Register your models here.

List_of_tokens = []
all_notifications = Notification_token.objects.values_list('token',flat=True,)
for i in all_notifications:
    List_of_tokens.append(i)
print(List_of_tokens)

def sendPush(title,content, registration_token, dataObject=None):
    
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title= title,
            body= content,
            image= 'https://x-eats.com/static/images/logo/logo%20-new.png',
        ),
        data=dataObject,
        tokens= List_of_tokens
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
        sendPush(obj.title, obj.content, List_of_tokens)
        obj.save()


class NotificationTokensAdmin(admin.ModelAdmin):
    model = Notification_token
    list_display = ('created','token','id')






admin.site.register(Push_Notification, pushNotiticationAdmin)
admin.site.register(Events,Event_Admin)
admin.site.register(Receipts, Receipts_Admin)
admin.site.register(Profile, Register)
admin.site.register(Team_Member, Team_Admin)
admin.site.register(TopCustomers, TopCustomers_Admin)
admin.site.register(Notification_token, NotificationTokensAdmin)
admin.site.register(Restaurant_Suggestion,Restaurant_Suggestion_Admin)


