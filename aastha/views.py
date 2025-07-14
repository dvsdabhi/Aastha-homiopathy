from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Appointment, Treatment, Blog, Patient, Review
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    treatment = Treatment.objects.order_by('?')[:3]
    reviews = Review.objects.order_by('?')[:3]

    context = {
        'total_treatments': treatment,
        'reviews': reviews,
    }
    return render(request,'index.html', context)

def about(request):
    return render(request,'about.html')

@login_required(login_url='patient_login')
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
            user = request.user,
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

@login_required(login_url='patient_login')
def my_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)
    print("appointments-",appointments)
    return render(request, 'my_appointments.html', {'appointments': appointments})

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
    blog_posts = Blog.objects.all()
    return render(request, 'blog.html', {'blog_posts': blog_posts})

def blog_detail(request, slug):
    blog = Blog.objects.get(id=slug)
    return render(request, 'blog_detail.html', {'blog': blog})

def patient_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        mobile   = request.POST.get('mobile')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('patient_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        Patient.objects.create(user=user, email=email, mobile=mobile)

        messages.success(request, 'Registration successful. Please login.')
        return redirect('patient_login')

    return render(request, 'patient_register.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, 'patient'):
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials or not a patient user')
            return redirect('patient_login')

    return render(request, 'patient_login.html')


def patient_logout(request):
    logout(request)
    return redirect('patient_login')

@login_required
def review_page(request):
    reviews = Review.objects.all().order_by('-created_at')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            # Check if user has already submitted a review
            existing_review = Review.objects.filter(user=request.user).first()

            if existing_review:
                # Update existing review
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, "Your review has been updated successfully.")
            else:
                # Create a new review
                Review.objects.create(
                    user=request.user,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Thank you! Your review has been submitted.")
            
            return redirect('review_page')

    return render(request, 'review_page.html', {'reviews': reviews})