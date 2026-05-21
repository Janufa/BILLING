"""
URL configuration for billing_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from billing_app.views import home_page, course_checkout, payment_success, courses_page, contact_page, bills_page, bill_detail

urlpatterns = [
    path('', home_page, name='home'),
    path('courses/', courses_page, name='courses'),
    path('course/<int:course_id>/checkout/', course_checkout, name='course_checkout'),
    path('payment-success/<str:bill_number>/', payment_success, name='payment_success'),
    path('contact/', contact_page, name='contact'),
    path('bills/', bills_page, name='bills'),
    path('bills/<str:bill_number>/', bill_detail, name='bill_detail'),
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/', include('billing_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
