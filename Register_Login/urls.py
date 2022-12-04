from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from Register_Login.views import Register, activate_user, email_activated, logOut, profile, signIn,email_sent,password_reset_emailing, team,events,about_us,get_users


app_name = 'Register_Login'

urlpatterns = [
    path('register', view = Register, name='Register'),
    path('login', view = signIn, name='login'),
    path('logOut',view = logOut, name='logOut'),
    path('email_sent', view = email_sent, name='email_sent'),
    path(route='activate/<token>', view=activate_user, name='activate'),
    path('email_activated', view = email_activated, name='email_activated'),
    path('team', view = team, name='team'),
    path('events',view = events, name = "events"),
    path('about_us',view = about_us, name = "about_us"),
    path('profile',view = profile, name = "profile"),



    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),



    path('password_reset/done/', view = password_reset_emailing ,name='password_reset_emailing'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),


    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # APIs URL
    path('get_users/', view= get_users, name='get_users'),
]

