"""
Views for the billing application API.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Course, Student, Enrollment, Payment, Bill
from .serializers import (
    UserSerializer, CourseSerializer, StudentSerializer,
    EnrollmentSerializer, PaymentSerializer, BillSerializer, RegistrationSerializer
)
from .utils.pdf_generator import generate_bill_pdf
from .utils.email_sender import send_bill_email
from decimal import Decimal


def home_page(request):
    """Render the public homepage with available courses."""
    courses = Course.objects.filter(is_active=True)
    return render(request, 'home.html', {'courses': courses})


def courses_page(request):
    """Explicit courses listing page (same as home for now)."""
    courses = Course.objects.filter(is_active=True)
    return render(request, 'home.html', {'courses': courses})


def contact_page(request):
    """Simple contact page."""
    return render(request, 'contact.html')


def bills_page(request):
    """List bills for the logged in student."""
    if not request.user.is_authenticated:
        return redirect('home')
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        return redirect('home')

    bills = Bill.objects.filter(enrollment__student=student)
    return render(request, 'bills_list.html', {'bills': bills})


def bill_detail(request, bill_number):
    bill = get_object_or_404(Bill, bill_number=bill_number)
    return render(request, 'bill_detail.html', {'bill': bill})


def course_checkout(request, course_id):
    """Render checkout form and process public course enrollment/payment."""
    course = get_object_or_404(Course, id=course_id, is_active=True)
    error_message = None

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        student_id = request.POST.get('student_id', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        payment_method = request.POST.get('payment_method', 'credit_card')
        # student_id may be omitted — auto-generate one below
        if not email or not first_name or not last_name:
            error_message = 'Please fill in all required fields.'
        else:
            # Auto-generate a unique student_id when not provided
            if not student_id:
                import uuid
                candidate = None
                while True:
                    candidate = f"STU{uuid.uuid4().hex[:8].upper()}"
                    if not Student.objects.filter(student_id=candidate).exists():
                        student_id = candidate
                        break
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            if created:
                user.set_unusable_password()
                user.save()
            else:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            # Handle existing Student by student_id. Allow auto-link when emails match.
            existing_by_id = Student.objects.filter(student_id=student_id).first()
            if existing_by_id:
                if existing_by_id.user == user:
                    student = existing_by_id
                    student_created = False
                    if phone and student.phone != phone:
                        student.phone = phone
                        student.save()
                else:
                    # If the student's linked user has the same email as provided, reassign to this user
                    if existing_by_id.user.email == email:
                        # Ensure current user doesn't already have a different student profile
                        try:
                            current_profile = user.student_profile
                            if current_profile != existing_by_id:
                                error_message = 'This account already has a different student profile. Please contact support to merge accounts.'
                                return render(request, 'course_checkout.html', {
                                    'course': course,
                                    'error_message': error_message,
                                })
                        except Student.DoesNotExist:
                            # Safe to reassign ownership of the Student record
                            existing_by_id.user = user
                            if phone:
                                existing_by_id.phone = phone
                            existing_by_id.save()
                            student = existing_by_id
                            student_created = False
                    else:
                        error_message = 'Student ID already registered with another account. Please login or use a different ID.'
                        return render(request, 'course_checkout.html', {
                            'course': course,
                            'error_message': error_message,
                        })
            else:
                student, student_created = Student.objects.get_or_create(
                    user=user,
                    defaults={
                        'student_id': student_id,
                        'phone': phone,
                    }
                )
                if not student_created and student.student_id != student_id:
                    student.student_id = student_id
                    student.phone = phone
                    student.save()

            enrollment = Enrollment.objects.filter(student=student, course=course).first()
            if enrollment and enrollment.is_paid:
                existing_bill = getattr(enrollment, 'bill', None)
                if existing_bill:
                    return redirect(reverse('payment_success', kwargs={'bill_number': existing_bill.bill_number}))
                error_message = 'You are already enrolled and paid for this course.'
            else:
                if not enrollment:
                    enrollment = Enrollment.objects.create(
                        student=student,
                        course=course,
                        amount=course.price,
                        status='pending'
                    )

                try:
                    from .utils.payment_gateway import process_mock_payment
                    transaction_id = process_mock_payment(enrollment.amount)

                    payment = Payment.objects.create(
                        enrollment=enrollment,
                        amount=enrollment.amount,
                        payment_method=payment_method,
                        transaction_id=transaction_id,
                        status='completed'
                    )

                    enrollment.is_paid = True
                    enrollment.status = 'active'
                    enrollment.paid_date = payment.payment_date
                    enrollment.save()
                    # Payment saved; signal `generate_bill_on_payment` will create the Bill and send email.
                    # Retrieve the bill created by the signal (post_save runs synchronously).
                    bill = Bill.objects.filter(enrollment=enrollment).first()
                    if bill:
                        return redirect(reverse('payment_success', kwargs={'bill_number': bill.bill_number}))
                    else:
                        # Fallback: if bill not created for some reason, display success and note.
                        return render(request, 'payment_success.html', {'bill': None, 'message': 'Payment processed. Bill is being generated.'})
                except Exception as exc:
                    error_message = str(exc)

    return render(request, 'course_checkout.html', {
        'course': course,
        'error_message': error_message,
    })


def payment_success(request, bill_number):
    """Render success page after payment and bill generation."""
    bill = get_object_or_404(Bill, bill_number=bill_number)
    if not bill.pdf_file:
        generate_bill_pdf(bill)
    return render(request, 'payment_success.html', {'bill': bill})


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Course model - read-only for students."""
    
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['level', 'instructor']
    search_fields = ['title', 'code', 'description']
    ordering_fields = ['price', 'title', 'created_at']


class StudentViewSet(viewsets.ViewSet):
    """ViewSet for Student registration and profile management."""
    
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new student."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Registration successful',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request):
        """Get student profile."""
        try:
            student = request.user.student_profile
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request):
        """Update student profile."""
        try:
            student = request.user.student_profile
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment management."""
    
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'is_paid']
    ordering_fields = ['enrollment_date']
    
    def get_queryset(self):
        """Return enrollments for the current student."""
        try:
            student = self.request.user.student_profile
            return Enrollment.objects.filter(student=student)
        except Student.DoesNotExist:
            return Enrollment.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Create new enrollment."""
        try:
            student = request.user.student_profile
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {'error': 'Already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            amount=course.price,
            status='pending'
        )
        
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment processing."""
    
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'payment_method']
    ordering_fields = ['payment_date']
    
    def get_queryset(self):
        """Return payments for the current student's enrollments."""
        try:
            student = self.request.user.student_profile
            return Payment.objects.filter(enrollment__student=student)
        except Student.DoesNotExist:
            return Payment.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Process payment and trigger bill generation."""
        try:
            student = request.user.student_profile
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        enrollment_id = request.data.get('enrollment_id')
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, student=student)
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'Enrollment not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Simulate payment processing
        from .utils.payment_gateway import process_mock_payment
        transaction_id = process_mock_payment(enrollment.amount)

        # Create payment record — signal will create the bill
        payment = Payment.objects.create(
            enrollment=enrollment,
            amount=enrollment.amount,
            payment_method=request.data.get('payment_method', 'credit_card'),
            transaction_id=transaction_id,
            status='completed'
        )

        # Update enrollment status
        enrollment.is_paid = True
        enrollment.status = 'active'
        enrollment.save()

        # Retrieve bill created by the post_save signal
        bill = Bill.objects.filter(enrollment=enrollment).first()

        serializer = self.get_serializer(payment)
        return Response({
            'payment': serializer.data,
            'bill': BillSerializer(bill).data if bill else None,
            'message': 'Payment successful; bill will be generated automatically.'
        }, status=status.HTTP_201_CREATED)


class BillViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Bill management."""
    
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'is_email_sent']
    ordering_fields = ['bill_date']
    
    def get_queryset(self):
        """Return bills for the current student's enrollments."""
        try:
            student = self.request.user.student_profile
            return Bill.objects.filter(enrollment__student=student)
        except Student.DoesNotExist:
            return Bill.objects.none()
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Download bill PDF."""
        bill = self.get_object()
        
        # Generate PDF if not exists
        if not bill.pdf_file:
            generate_bill_pdf(bill)
        
        if bill.pdf_file:
            return FileResponse(bill.pdf_file.open('rb'), content_type='application/pdf')
        
        return Response(
            {'error': 'PDF not available'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    @action(detail=True, methods=['post'])
    def send_email(self, request, pk=None):
        """Send bill via email."""
        bill = self.get_object()
        
        # Generate PDF if not exists
        if not bill.pdf_file:
            generate_bill_pdf(bill)
        
        # Send email
        send_bill_email(bill)
        bill.is_email_sent = True
        bill.save()
        
        return Response(
            {'message': 'Bill sent via email'},
            status=status.HTTP_200_OK
        )
