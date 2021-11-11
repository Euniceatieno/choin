from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UpdateProfileForm,UserProfileForm
from .models import Redeem, RewardedItem, Student
from django.core.exceptions import ObjectDoesNotExist
from leadership.models import RedeemableItem, Transaction, User, Wallet
from django.http import JsonResponse
import json
from .models import  *
from django.core.exceptions import ObjectDoesNotExist
from leadership.models import RedeemableItem, Transaction, Wallet


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

def student_home(request):
    return render(request,'student_home.html')

    
def redeem(request):
    if request.user.is_authenticated:
        student_customer = Student.objects.get(user = request.user)
        # student_customer = Student.objects.get(id=request.user.id)
        order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
        items = order.rewardeditem_set.all()
        cartItems = order.calculate_cart_items
    else:
        items= []
        order={'get_cart_total':0,'get_cart_items':0}
        # cartItems = order['get_cart_items']
    reward_items=RedeemableItem.objects.all()
    bal = Wallet.objects.all().filter(owner = request.user)
    for reward in reward_items:
        if reward.activate_page == False:
            return render(request,'inactive_redeem.html',{'bal':bal, 'items':items})
    return render(request,'redeem.html',{'reward_items':reward_items,'bal':bal, 'items':items, 'cartItems':cartItems})
    

def redeem_failed(request):
    bal = Wallet.objects.all().filter(owner = request.user)
    return render(request,'RedeemFailed.html',{'bal':bal})

def redeem_success(request):
    if request.user.is_authenticated:
        student_customer = Student.objects.get(user = request.user)
        order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
        items = order.rewardeditem_set.all()
      
    else:
        items= []
    context = {'items':items, 'order':order}  
    return render(request,'RedeemSucceed.html',context)

def cart(request):
    bal = Wallet.objects.all().filter(owner = request.user)
    if request.user.is_authenticated:
        student_customer = Student.objects.get(user = request.user)

        order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
        items = order.rewardeditem_set.all()
        print(items)
     
    else:
        items= []


        order={'calculate_cart_total':0, 'calculate_cart_items':0}
    

    context = {'items':items, 'order':order,'bal':bal}    
    return render(request,'cart.html', context)
    

def redeem_active(request):
    return render(request,'redeem_active.html')
def student_dashboard(request):
    student=Student.objects.get(user=request.user)
    choin_balance=Wallet.objects.get(owner=request.user)
    data={'student':student,'choin_balance':choin_balance}
    return render(request,'stud_dashboard.html')

def student_transactions(request):
    transactions = Transaction.objects.all().filter(receiver = request.user.username)
    bal = Wallet.objects.all().filter(owner = request.user)
    return render(request,'student_transactions.html',{'transactions':transactions,'bal':bal})  

# def view_redeemed_items(request):
#     if request.user.is_authenticated:
#         customer=request.user.idt
#         order,created=Order.objects.get_or_create(customer=customer,completed=False)
#         items=order.orderedproduct_set.all()
#     else:
#         items=[]

#     return render(request,'student_transactions.html',{'transactions':transactions,'bal':bal})  

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId'] 
    action = data['action']

    student_customer = Student.objects.get(user = request.user)
    product = RedeemableItem.objects.get(id=productId)
    order, created = Redeem.objects.get_or_create(student=student_customer, complete = False)
    orderItem, created = RewardedItem.objects.get_or_create(order = order, reward=product )

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
         orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.student = Student.objects.get(user=request.user)
    orderItem.save()

    if orderItem.quantity <= 0:
       orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def student_redeem(request):
    bal = Wallet.objects.all().filter(owner = request.user)
    std = Student.objects.get(user = request.user)
    order = Redeem.objects.all().filter(student = std)
    the_balance=None
    for b in bal:
        for ord in order:

            if b.choinBalance < ord.calculate_cart_total:
                return redirect('redeem_failed')
            else:
     
                wallets=Wallet.objects.all().filter(owner=request.user)
                the_balance =b.choinBalance - ord.calculate_cart_total
                red = Redeem.objects.all().filter(student = std)
                red.delete()
                
                
                wallets.update(owner = request.user, choinBalance = the_balance)

    return render(request,'RedeemSucceed.html',{'the_balance':the_balance,'order':order}) 

def myItems(request):
    return render(request,'my_items.html')         












    

# def mark_as_read(request,pk):
    
#     notifications = Notifications.objects.get(pk=pk)
#     notifications.mark_as_read()
#     return redirect(reverse('student-home'))


