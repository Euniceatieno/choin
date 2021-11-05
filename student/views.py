from django.shortcuts import redirect, render
from .forms import UpdateProfileForm,UserProfileForm
from .models import Student
from django.core.exceptions import ObjectDoesNotExist
from leadership.models import RedeemableItem
from leadership.models import Transaction,Wallet
# @login_required



def student_profile(request):
    try:
        userprofile = request.user.userprofile
    except ObjectDoesNotExist:
        userprofile = Student(user=request.user)
        
    if request.method == 'POST':
        user_form = UpdateProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile.user)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            #user.username = user.email
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('student-home')
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
        user_form = UpdateProfileForm(instance=request.user)
    args = {
        'user_form': user_form, # basic user form
        'profile_form': profile_form # user profile form
        }
    return render(request, 'student_profile.html', args)

def student_transactions(request):
    transactions = Transaction.objects.all().filter(receiver = request.user.username)
    bal = Wallet.objects.all().filter(owner = request.user)
    
    

    return render(request,'student_transactions.html',{'transactions':transactions,'bal':bal})     

def student_home(request):
    return render(request,'student_home.html')
def redeem(request):
    reward_items=RedeemableItem.objects.all()
    
    bal = Wallet.objects.all().filter(owner = request.user.id)
    return render(request,'redeem.html',{'reward_items':reward_items,'bal':bal})
def redeem_failed(request):
    return render(request,'RedeemFailed.html')
def redeem_success(request):
    return render(request,'RedeemSucceed.html')