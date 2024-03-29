from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from gfg import settings
from . tokens import generate_token
from .html_forms import SignIn_Form
from .html_forms import SignUp_Form

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        form = SignUp_Form(request.POST)

        # Check if form is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            email = form.cleaned_data['email']
            pass1 = form.cleaned_data['pass1']
            pass2 = form.cleaned_data['pass2']

            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('signup')
        
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!")
                return redirect('signup')
        
            if pass1 != pass2:
                messages.error(request, "Passwords don't match!")
                return redirect('signup')
        
            if not username.isalnum():
                messages.error(request, "Username must be Alphanumeric!!")
                return redirect('signup')
        
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
            # Welcome Email
            subject = "Welcome to AAGroup Login!!"
            message = "Hello " + myuser.first_name + "!! \n" + "Welcome to AAGroup!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAAGroup"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
        
            email = EmailMessage(
                subject,
                message,
                from_email,
                to_list,
            )
            email.fail_silently = True
            email.send()

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email @ AAGroup - AAGroup Login!!"
            context = {
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            } 
            message2 = render_to_string('email_confirmation.html', context)

            email2 = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email2.fail_silently = True
            email2.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        
        form = SignIn_Form(request.POST)
        
        # Check if form is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            pass1 = form.cleaned_data['pass1']

            user = authenticate(username=username, password=pass1)

            if user is not None:
                login(request, user)
                fname = user.first_name
                messages.success(request, "Logged In Sucessfully!!")
                return render(request, "authentication/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')
