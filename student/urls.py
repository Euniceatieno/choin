from django.urls import path
from . views import redeem,student_profile,student_home,redeem_failed,redeem_success, student_transactions
# from core.views import Profile
urlpatterns =[
    path('student-home',student_home,name='student-home'),
    path('redeem/',redeem,name='redeem'),
    path('student-profile/',student_profile,name='student-profile'),
    path('redeem_failed/',redeem_failed,name='redeem_failed'),
    path('redeem_success/',redeem_success,name='redeem_success'),
     path('student_transactions/',student_transactions,name='student_transactions'),
    ]