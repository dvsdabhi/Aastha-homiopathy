from django.contrib import admin
from .models import*
from django.core.mail import send_mail
from django.conf import settings

# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(TreatmentCategory)
admin.site.register(Treatment)
admin.site.register(Blog)
admin.site.register(Patient)
admin.site.register(Review)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date', 'time', 'is_confirmed']
    list_filter = ['is_confirmed']

    def save_model(self, request, obj, form, change):
        # Check if appointment is newly confirmed
        if 'is_confirmed' in form.changed_data and obj.is_confirmed:
            subject = 'Appointment Confirmed - Aastha Homeopathy'
            message = f'''
                Dear {obj.name},

                Your appointment has been confirmed.

                Doctor: {obj.doctor}
                Date: {obj.date}
                Time: {obj.time.strftime('%H:%M')}

                We look forward to seeing you.

                Regards,
                Aastha Homeopathy
                '''
            send_mail(
                subject,
                message,
                'yourclinicemail@example.com',  # Replace with your FROM email
                [obj.email],
                fail_silently=False,
            )

        super().save_model(request, obj, form, change)

admin.site.register(Appointment, AppointmentAdmin)