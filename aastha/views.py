from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, AppointmentForm
from .models import Appointment, Treatment , Blog
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime

# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('phone')
        doctor = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')

        # Parse date and time
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            time_obj = datetime.strptime(time, '%H:%M').time()
        except:
            messages.error(request, 'Invalid date or time format.')
            return redirect('appointment')

        # Check for conflict (30-minute window)
        conflict = Appointment.objects.filter(
            date=date_obj,
            time=time_obj
        ).exists()

        if conflict:
            messages.error(request, 'This slot is already booked. Please choose another.')
            return redirect('appointment')

        # Save appointment
        Appointment.objects.create(
            name=name,
            email=email,
            phone=mobile,
            doctor=doctor,
            date=date_obj,
            time=time_obj,
            message=message
        )

        # Send confirmation email
        subject = 'Appointment Received - Aastha Homeopathy'
        body = f'''Dear {name},

            Thank you for booking an appointment with Aastha Homeopathy.

            Here are your appointment details:
            Doctor: {doctor}
            Date: {date}
            Time: {time}

            We will confirm your appointment soon.

            Regards,
            Aastha Homeopathy
            '''
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])

        messages.success(request, 'Appointment booked successfully! Check your email for details.')
        return redirect('appointment')
    return render(request, 'appointment.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
    return render(request,'contact.html')

def feature(request):
    return render(request,'feature.html')

def treatment(request):
    treatments = Treatment.objects.all()
    return render(request, 'treatment.html', {'treatments': treatments})


def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')

def not_found(request):
    return render(request,'404.html')

def treatment_detail_view(request, slug):
    treatment = Treatment.objects.get(id=slug)
    return render(request, 'treatment_detail.html', {'treatment': treatment})

def blog_view(request):
    blog_posts = [
        {
            "model": "yourapp.blogpost",
            "pk": 1,
            "fields": {
            "title": "Homeopathy Treatment for Migraine",
            "slug": "1",
            "content": "<p>Homeopathy offers long-term relief from migraines...</p>",
            "image": "blog_images/default.jpg",
            "author": "Dr. Priyank Shekhaliya",
            "created_at": "2025-06-30T10:00:00Z"
            }
        },
        {
            "model": "yourapp.blogpost",
            "pk": 2,
            "fields": {
            "title": "Benefits of Natural Healing",
            "slug": "2",
            "content": "<p>Natural healing through homeopathy has shown great benefits...</p>",
            "image": "blog_images/default.jpg",
            "author": "Dr. Priyank Shekhaliya",
            "created_at": "2025-06-28T10:00:00Z"
            }
        }
    ]
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def blog_detail(request, slug):
    blog = {
        "model": "yourapp.blogpost",
        "pk": 1,
        "fields": {
        "title": "Homeopathy Treatment for Migraine",
        "slug": "1",
        "content": "<p>Homeopathy offers long-term relief from migraines...</p>",
        "image": "blog_images/default.jpg",
        "author": "Dr. Priyank Shekhaliya",
        "created_at": "2025-06-30T10:00:00Z"
        }
    }
    return render(request, 'blog_detail.html', {'blog': blog})