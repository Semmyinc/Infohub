from django.shortcuts import render, redirect
from .models import ContactMessage
from django.http import HttpResponseRedirect

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        client_message = ContactMessage()
        client_message.name = request.POST['name']
        client_message.email = request.POST['email']
        client_message.subject = request.POST['subject']
        client_message.message = request.POST['message']
        client_message.save()
       
        user = request.user
       # User Message Receipt Notifictation
        current_site = get_current_site(request)
        mail_subject = 'Message receipt Notification'
        message = render_to_string('team/message_acknowledgement_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # messages.success(request, f'Thank you for registering. Verification mail has been sent to your email for confirmation.')
        return HttpResponseRedirect(request.path)

    context = {}
    return render(request, 'contact.html', context)

def about(request):
    context = {}
    return render(request, 'about.html', context)