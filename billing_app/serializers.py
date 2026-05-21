"""
Serializers for the billing application API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Student, Enrollment, Payment, Bill


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model."""
    
    enrolled_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'code', 'level', 'price', 
                 'duration_weeks', 'instructor', 'max_students', 'enrolled_count', 'is_active']
    
    def get_enrolled_count(self, obj):
        """Get the count of enrolled students."""
        return obj.enrollments.filter(status__in=['active', 'completed']).count()


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model."""
    
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'user', 'username', 'email', 'phone', 
                 'address', 'city', 'state', 'zipcode', 'date_of_birth', 'is_active']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model."""
    
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'course_id', 'enrollment_date', 
                 'status', 'amount', 'is_paid', 'paid_date']
        read_only_fields = ['student', 'enrollment_date', 'amount']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    
    enrollment = EnrollmentSerializer(read_only=True)
    enrollment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'enrollment', 'enrollment_id', 'amount', 'payment_method', 
                 'transaction_id', 'status', 'payment_date', 'processed_date', 'notes']
        read_only_fields = ['payment_date', 'processed_date']


class BillSerializer(serializers.ModelSerializer):
    """Serializer for Bill model."""
    
    enrollment = EnrollmentSerializer(read_only=True)
    student_name = serializers.SerializerMethodField()
    course_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Bill
        fields = ['id', 'enrollment', 'bill_number', 'bill_date', 'due_date', 
                 'amount', 'tax', 'total_amount', 'status', 'student_name', 
                 'course_name', 'is_email_sent', 'email_sent_date', 'pdf_file']
        read_only_fields = ['bill_number', 'bill_date', 'student_name', 'course_name']
    
    def get_student_name(self, obj):
        """Get student full name."""
        return obj.enrollment.student.user.get_full_name()
    
    def get_course_name(self, obj):
        """Get course title."""
        return obj.enrollment.course.title


class RegistrationSerializer(serializers.Serializer):
    """Serializer for student registration."""
    
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    student_id = serializers.CharField(max_length=50)
    
    def validate(self, data):
        """Validate registration data."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already registered."})
        
        if Student.objects.filter(student_id=data['student_id']).exists():
            raise serializers.ValidationError({"student_id": "Student ID already exists."})
        
        return data
    
    def create(self, validated_data):
        """Create new user and student profile."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        Student.objects.create(
            user=user,
            student_id=validated_data['student_id'],
            phone=validated_data.get('phone', '')
        )
        
        return user
