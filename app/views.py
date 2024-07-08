from django.shortcuts import render,redirect
from .models import Table_1
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
#below import is done for sending emails
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.core.mail import EmailMessage

# Create your views here.
def index(request):
    return render(request,"index.html")

def video(request):
    return render(request,"video.html")

def video1(request):
    return render(request,"video1.html")

def video2(request):
    return render(request,"video2.html")

def order(request):
    if request.method=="POST":
        name=request.POST.get('name')
        flavour=request.POST.get('flavour')
        topings=request.POST.get('topings')
        address=request.POST.get('address')
        phno=request.POST.get('phno')
        email=request.POST.get('email')
        time=request.POST.get('time')
        quantity=request.POST.get('quantity')
        query=Table_1(name=name,flavour=flavour,topings=topings,address=address,phno=phno,email=email,time=time,quantity=quantity)
        query.save ()
        #email sending starts from here
        from_email=settings.EMAIL_HOST_USER
        connection=mail.get_connection()
        connection.open()
        email_message=mail.EmailMessage(f'Email is from {name}',f'UserEmail : {email}\nUserPhoneNumber: {phno}\n ADDRESS : {address} \nQUANTITY: {quantity} \nFLAVOUR: {flavour} \nTOPINGS: {topings} \nTIME: {time}' ,from_email,['sabap600@gmail.com','frostyscoopicecreamhouse@gmail.com'],connection=connection)
        connection.close()
        email_client=mail.EmailMessage('Frosty Scoops Online Store Response','Thanks For ordering from Us we will deliver your product at your doorstep payment is accepted at that time \n\nFrostyScoopIceCreamHouse\n0657-23345',from_email,[email],connection=connection)
        connection.send_messages([email_message,email_client])
        messages.info(request,"Thanks for Ordering! We will reach out you!!")
        return redirect("/order")
    return render(request,"index.html")

def handlesignup(request):
    if request.method=="POST":
        username=request.POST.get('uname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password!=cpassword:
            messages.warning(request,"Password is incorrect")
            return redirect("/signup")
        try:
            if User.objects.get(username=username):
                return redirect("/signup")
        except:
            pass
        try:
            if User.objects.get(email=email):
                return redirect("/signup")
        except:
            pass
        query=User.objects.create_user(username=username,email=email,password=password)
        query.save()
        return redirect("/login")
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":
        username=request.POST.get('uname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        myuser=authenticate(username=username,password=password,email=email)
        if myuser is not None:
            login(request,myuser)
            return redirect("/")
        else:
            return redirect("/login")
    return render(request,"login.html")    
    
def handlelogout(request):    
    logout(request)
    return redirect("/login")
