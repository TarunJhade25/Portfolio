from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from .forms import ContactForm
from django.core.mail import send_mail  # Import send_mail
from django.conf import settings


def home(request):
    return render (request,"home.html")

def about(request):
    return render (request,"about.html")

def projects(request):
    projects_show=[
        {
            'title': 'Rasoi Connect',
            'path': 'images/rasoi_connect.PNG',
        },
        {
            'title': 'Ecommerce',
            'path': 'images/ecommerce.PNG',
        },

        {
            'title': 'Timetable Scheduler',
            'path': 'images/timtable.PNG',
        },
        {
            'title': 'CRUD',
            'path': 'images/CRUD.PNG',
        },


    ]
    return render (request,"projects.html",{"projects_show": projects_show})

def certificates(request):
    return render (request,"certificates.html")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get cleaned form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            
            # Build the email content
            email_subject = f"New Contact Form Submission from {name}"
            email_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
            
            # Send the email
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,  # From email
                [settings.DEFAULT_FROM_EMAIL],  # To email (your email)
                fail_silently=False,
            )
            
            return HttpResponse("Thank you for contacting us!")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def resume(request):
    resume_path="myresume/resume.pdf"
    resume_path=staticfiles_storage.path(resume_path)
    if staticfiles_storage.exists(resume_path):
        with open(resume_path,"rb") as resume_file:
            response=HttpResponse(resume_file.read(),content_type="application/pdf")
            response['Content-Disposition']='attachment';filename="resume.pdf"
            return response
    else:
        return HttpResponse("Resume Not Found!!!", status=404)
    