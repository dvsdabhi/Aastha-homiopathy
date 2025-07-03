from django.shortcuts import render, get_object_or_404, redirect
from aastha.models import Appointment, ContactMessage,  Treatment, TreatmentCategory, Blog
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@staff_member_required
@login_required(login_url='admin_login')
def dashboard(request):
    total_appointments = Appointment.objects.count()
    confirmed_appointments = Appointment.objects.filter(is_confirmed=True).count()
    total_treatments = Treatment.objects.count()
    total_blogs = Blog.objects.count()
    total_categories = TreatmentCategory.objects.count()
    contact = ContactMessage.objects.count()

    context = {
        'total_appointments': total_appointments,
        'confirmed_appointments': confirmed_appointments,
        'total_treatments': total_treatments,
        'total_blogs': total_blogs,
        'total_categories': total_categories,
        'total_contact':contact
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
@login_required(login_url='admin_login')
def appointments(request):
    appointments = Appointment.objects.all().order_by('-date')
    return render(request, 'admin_appointments.html', {'appointments': appointments})

@staff_member_required
@login_required
@user_passes_test(lambda u: u.is_superuser)
def confirm_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)

    if request.method == 'POST' and not appointment.is_confirmed:
        appointment.is_confirmed = True
        appointment.save()

        # ✅ Send confirmation email
        subject = 'Appointment Confirmed - Aastha Homeopathy'
        message = f'''
            Dear {appointment.name},

            Your appointment has been confirmed.

            Doctor: {appointment.doctor}
            Date: {appointment.date}
            Time: {appointment.time.strftime('%H:%M')}

            We look forward to seeing you.

            Regards,
            Aastha Homeopathy
            '''
        send_mail(
            subject,
            message,
            'priyankshekhliya@gmail.com',
            [appointment.email],
            fail_silently=False,
        )

    return redirect('admin_appointments')

@staff_member_required
@login_required(login_url='admin_login')
def treatments(request):
    query = request.GET.get('q', '')
    categories = TreatmentCategory.objects.prefetch_related('treatments')
    if query:
        for category in categories:
            category.treatments_filtered = category.treatments.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
    else:
        for category in categories:
            category.treatments_filtered = category.treatments.all()

    return render(request, 'admin_treatment.html', {
        'categories': categories,
        'query': query
    })

@staff_member_required
@login_required(login_url='admin_login')
def add_treatment(request):
    categories = TreatmentCategory.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        category = TreatmentCategory.objects.get(id=category_id)

        Treatment.objects.create(
            title=title,
            description=description,
            category=category,
            image=image
        )
        return redirect('admin_treatments')

    return render(request, 'admin_add_treatment.html', {'categories': categories})

@staff_member_required
@login_required(login_url='admin_login')
def update_treatment(request, id):
    treatment = get_object_or_404(Treatment, id=id)
    categories = TreatmentCategory.objects.all()

    if request.method == 'POST':
        treatment.title = request.POST.get('title')
        treatment.description = request.POST.get('description')
        category_id = request.POST.get('category')
        treatment.category = TreatmentCategory.objects.get(id=category_id)

        if request.FILES.get('image'):
            treatment.image = request.FILES['image']

        treatment.save()
        return redirect('admin_treatments')

    return render(request, 'admin_update_treatment.html', {
        'treatment': treatment,
        'categories': categories
    })

@staff_member_required
@login_required(login_url='admin_login')
def delete_treatment(request, id):
    treatment = get_object_or_404(Treatment, id=id)
    treatment.delete()
    return redirect('admin_treatments')

@staff_member_required
@login_required(login_url='admin_login')
def blogs(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'admin_blog.html', {'blogs': blogs, 'query': query})

@staff_member_required
@login_required(login_url='admin_login')
def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Blog.objects.create(
            title=title,
            content=content,
            image=image
        )
        return redirect('admin_blogs')

    return render(request, 'admin_add_blog.html')

@staff_member_required
@login_required(login_url='admin_login')
def update_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        if request.FILES.get('image'):
            blog.image = request.FILES.get('image')
        blog.save()
        return redirect('admin_blogs')

    return render(request, 'admin_update_blog.html', {'blog': blog})

@staff_member_required
@login_required(login_url='admin_login')
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    return redirect('admin_blogs')

def login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  # if already logged in
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid credentials"
            return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

@staff_member_required
@login_required(login_url='admin_login')
def contact(request):
    contact = ContactMessage.objects.all()
    return render(request, 'admin_contact.html', {'contact' : contact})

def logout_view(request):
    logout(request)
    return redirect('admin_login')