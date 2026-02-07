from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProfileForm, UserForm, AddUserForm
from.models import Users, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
from stories.models import Category, Blog
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

# for verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def adduser(request):
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(request.POST or None)
        if form.is_valid():
            # name = form.cleaned_data['first_name']
            user = form.save()
            name = user.first_name
            messages.success(request, f"{name}'s account has been created successfully")
            return redirect('dashboard_users') 
        # messages.error(request, f'error occured while filling form. Please try again')
        # return print(form.errors) 
        # If form is invalid, we DON'T redirect. 
        # We let it fall through so the user sees the specific field errors.
        messages.error(request, "Please correct the errors below.")

    context = {'form':form}
    return render(request, 'users/adduser.html', context)  

def edituser(request, pk):
    user = get_object_or_404(Users, id=pk)
    if request.method == 'POST':
        form = AddUserForm(request.POST or None, instance=user)
        if form.is_valid():
            name = form.cleaned_data['first_name']
            form.save()
            messages.success(request, f'{name}\'s account has been updated successfully')
            return redirect('dashboard_users') 
        
        messages.error(request, f'Please correct the errors below')
        # return redirect('dashboard_users') 

    form = AddUserForm(instance=user)
    context = {'form':form}
    return render(request, 'users/edituser.html', context)

def deleteuser(request, pk):
    user = get_object_or_404(Users, id=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'user account has been deleted successfully')
        return redirect('dashboard_users')

    context = {'user':user}
    return render(request, 'users/deleteuser.html', context)


def dashboard(request):
    categories = Category.objects.all()
    stories = Blog.objects.all()
    users = Users.objects.all()
    category_count = categories.count()
    story_count = stories.count()
    user_count = users.count()
    context = {'category_count':category_count, 'story_count':story_count, 'user_count':user_count}
    return render(request, 'users/dashboard.html', context)

def dashboard_categories(request):
    context = {}
    return render(request, 'users/dashboard_categories.html', context)

def dashboard_stories(request):
    stories = Blog.objects.all()

    context = {'stories':stories}
    return render(request, 'users/dashboard_stories.html', context)

# def is_manager(user):
#     manager = user.groups.filter(name='manager').exists()
#     return manager

# @user_passes_test(is_manager)
def dashboard_users(request):
    users = Users.objects.all()

    context = {'users':users}
    return render(request, 'users/dashboard_users.html', context)

def register(request):
    form = RegisterForm()
    if request.method =='POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            
            username = form.cleaned_data['username']
            if username == None:
                username = email.split('@')[0]
            
            user = Users.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone = phone
            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Account Activation Notification'
            message = render_to_string('users/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, f'Thank you for registering. Verification mail has been sent to your email for confirmation.')
            # return redirect('/users/login/?command=verification&email='+email)
            return redirect('home')

    
    context = {'form':form}
    return render(request, 'users/register.html', context)


def activate(request, uidb64, token):
    # return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Users._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'congrats! Account successfully verified and activated')
        return redirect('login')
    
    else:
        messages.info(request, f'Invalid Activation Link')
        return redirect('register')
    
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user != None:
            login(request, user)
            messages.success(request, f'Welcome! Glad to have you back')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
           

                print('query: ', query)
                # query:  next=/payment/checkout/
                # print('_________')
                params = dict(x.split('=') for x in query.split('&'))
                # print('params: ', params)
                # params:  {'next': '/payment/checkout/'}
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
                
            except:
                return redirect('dashboard')
        else:
            # messages.info(request, f'Invalid login credentials. Please check and try again.')
            return redirect('login')
    
   
    return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, f'You just logged out. See you around!')
    return redirect('login')

def profile(request):
    profile = Profile.objects.get(user__id = request.user.id)
    user = Users.objects.get(id=request.user.id)
    userform = UserForm()
    profileform = ProfileForm()
    if request.method == 'POST':
        userform = UserForm(request.POST, instance=user)
        profileform = ProfileForm(request.POST, request.FILES, instance=profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request, f'Profile updated successfully')

    userform = UserForm(instance=user)
    profileform = ProfileForm(instance=profile)
    context = {'userform':userform, 'profileform':profileform}
    return render(request, 'users/profile.html', context)

def other_user_profile(request, pk):
    other_user_profile = get_object_or_404(Profile, user__id=pk)
    other_user = get_object_or_404(Users, id=pk)
    context = {'other_user_profile':other_user_profile, 'other_user': other_user}
    return render(request, 'users/other_user_profile.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        # check if mail is in database
        if Users.objects.filter(email=email).exists:
            user = Users.objects.get(email__iexact=email)

            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Password Reset Notification'
            message = render_to_string('users/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send() 

            messages.success(request, f'Password reset link has been sent to your email.')
            return redirect('login')
        else:
            messages.warning(request, f'Email does not exist in our database. Please check and try again')
            return redirect('forgot_password')   
    context = {}
    return render(request, 'users/forgot_password.html', context)

def reset_password_validation(request, uidb64, token):
    # return HttpResponse('ok')
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Users._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Users.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, f'Please reset your password')
        return redirect('reset_password')
    else:
        messages.warning(request, f'Password reset link has expired. please try again')
        return redirect('forgot_password')
    

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Users.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, f'Password Reset Completed')
            return redirect('login')
        else:
            messages.success(request, f'Passwords mis-match. Please try again')
            return redirect('reset_password')
    else:
        return render(request, 'users/reset_password.html')
