"""
Admin configuration for billing application.
"""
from django.contrib import admin
from .models import Course, Student, Enrollment, Payment, Bill


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for Course model."""
    
    list_display = ['code', 'title', 'price', 'instructor', 'level', 'is_active']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['code', 'title', 'instructor']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Course Information', {
            'fields': ('code', 'title', 'description', 'level')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration_weeks')
        }),
        ('Instructor & Capacity', {
            'fields': ('instructor', 'max_students')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin configuration for Student model."""
    
    list_display = ['student_id', 'get_full_name', 'phone', 'city', 'is_active']
    list_filter = ['is_active', 'enrollment_date', 'city']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['enrollment_date']
    fieldsets = (
        ('User Profile', {
            'fields': ('user',)
        }),
        ('Student Details', {
            'fields': ('student_id', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zipcode')
        }),
        ('Status', {
            'fields': ('is_active', 'enrollment_date'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        """Get student full name."""
        return obj.user.get_full_name()
    
    get_full_name.short_description = 'Full Name'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin configuration for Enrollment model."""
    
    list_display = ['get_student_id', 'get_course_code', 'status', 'amount', 'is_paid', 'enrollment_date']
    list_filter = ['status', 'is_paid', 'enrollment_date']
    search_fields = ['student__student_id', 'course__code', 'course__title']
    readonly_fields = ['enrollment_date', 'amount']
    fieldsets = (
        ('Enrollment Details', {
            'fields': ('student', 'course', 'enrollment_date')
        }),
        ('Payment Information', {
            'fields': ('amount', 'is_paid', 'paid_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )
    
    def get_student_id(self, obj):
        """Get student ID."""
        return obj.student.student_id
    
    get_student_id.short_description = 'Student ID'
    
    def get_course_code(self, obj):
        """Get course code."""
        return obj.course.code
    
    get_course_code.short_description = 'Course Code'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for Payment model."""
    
    list_display = ['transaction_id', 'get_enrollment_info', 'amount', 'status', 'payment_method', 'payment_date']
    list_filter = ['status', 'payment_method', 'payment_date']
    search_fields = ['transaction_id', 'enrollment__student__student_id', 'enrollment__course__code']
    readonly_fields = ['payment_date', 'processed_date']
    fieldsets = (
        ('Payment Details', {
            'fields': ('enrollment', 'transaction_id')
        }),
        ('Amount & Method', {
            'fields': ('amount', 'payment_method')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Dates', {
            'fields': ('payment_date', 'processed_date'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_enrollment_info(self, obj):
        """Get enrollment info."""
        return f"{obj.enrollment.student.student_id} - {obj.enrollment.course.code}"
    
    get_enrollment_info.short_description = 'Enrollment'


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Admin configuration for Bill model."""
    
    list_display = ['bill_number', 'get_enrollment_info', 'total_amount', 'status', 'is_email_sent', 'bill_date']
    list_filter = ['status', 'is_email_sent', 'bill_date']
    search_fields = ['bill_number', 'enrollment__student__student_id', 'enrollment__course__code']
    readonly_fields = ['bill_number', 'bill_date']
    fieldsets = (
        ('Bill Information', {
            'fields': ('bill_number', 'enrollment')
        }),
        ('Billing Dates', {
            'fields': ('bill_date', 'due_date')
        }),
        ('Amount Details', {
            'fields': ('amount', 'tax', 'total_amount')
        }),
        ('Status & Email', {
            'fields': ('status', 'is_email_sent', 'email_sent_date')
        }),
        ('PDF & Notes', {
            'fields': ('pdf_file', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def get_enrollment_info(self, obj):
        """Get enrollment info."""
        return f"{obj.enrollment.student.student_id} - {obj.enrollment.course.code}"
    
    get_enrollment_info.short_description = 'Enrollment'
