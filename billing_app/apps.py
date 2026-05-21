"""
Application configuration for billing_app.
"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BillingAppConfig(AppConfig):
    """Configuration class for billing_app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billing_app'
    verbose_name = 'Billing System'
    
    def ready(self):
        """Import signals and connect default course seeding after migrations."""
        import billing_app.signals  # noqa
        post_migrate.connect(self._load_default_courses, sender=self)

    def _load_default_courses(self, sender, **kwargs):
        """Seed default courses if none exist."""
        try:
            from django.db.utils import OperationalError, ProgrammingError
            from .models import Course

            default_courses = [
                {
                    'title': 'Python Programming Basics',
                    'description': 'Learn Python fundamentals, syntax, and practical programming skills.',
                    'code': 'PY101',
                    'level': 'beginner',
                    'price': 199.00,
                    'duration_weeks': 10,
                    'instructor': 'James Carter',
                    'max_students': 100,
                    'is_active': True,
                },
                {
                    'title': 'Web Development with Django',
                    'description': 'Build full-stack web applications using Django and REST APIs.',
                    'code': 'DJG201',
                    'level': 'intermediate',
                    'price': 299.00,
                    'duration_weeks': 12,
                    'instructor': 'Anna Patel',
                    'max_students': 80,
                    'is_active': True,
                },
                {
                    'title': 'Data Science Essentials',
                    'description': 'Explore data analysis, visualization, and machine learning basics.',
                    'code': 'DS301',
                    'level': 'advanced',
                    'price': 349.00,
                    'duration_weeks': 14,
                    'instructor': 'Megan Lee',
                    'max_students': 60,
                    'is_active': True,
                },
                {
                    'title': 'Cloud Architecture Mastery',
                    'description': 'Design scalable cloud systems and deploy resilient applications.',
                    'code': 'CLD401',
                    'level': 'intermediate',
                    'price': 279.00,
                    'duration_weeks': 11,
                    'instructor': 'Samuel Rivera',
                    'max_students': 70,
                    'is_active': True,
                },
                {
                    'title': 'AI & Machine Learning',
                    'description': 'Build intelligent models with modern ML tools and workflows.',
                    'code': 'AI501',
                    'level': 'advanced',
                    'price': 399.00,
                    'duration_weeks': 16,
                    'instructor': 'Priya Nair',
                    'max_students': 50,
                    'is_active': True,
                },
                {
                    'title': 'UI/UX Design Studio',
                    'description': 'Create polished user experiences with design thinking and prototyping.',
                    'code': 'UX601',
                    'level': 'beginner',
                    'price': 229.00,
                    'duration_weeks': 9,
                    'instructor': 'Nina Walker',
                    'max_students': 90,
                    'is_active': True,
                },
                {
                    'title': 'Cybersecurity Fundamentals',
                    'description': 'Secure applications and infrastructure with modern cybersecurity practices.',
                    'code': 'CYB701',
                    'level': 'intermediate',
                    'price': 319.00,
                    'duration_weeks': 12,
                    'instructor': 'Amina Hassan',
                    'max_students': 65,
                    'is_active': True,
                },
                {
                    'title': 'Digital Marketing Pro',
                    'description': 'Master digital strategy, SEO, and campaign analytics for modern brands.',
                    'code': 'DMK801',
                    'level': 'beginner',
                    'price': 219.00,
                    'duration_weeks': 8,
                    'instructor': 'Laura Chen',
                    'max_students': 85,
                    'is_active': True,
                },
                {
                    'title': 'DevOps Engineering',
                    'description': 'Automate infrastructure, pipelines, and deployment workflows with DevOps best practices.',
                    'code': 'DOP901',
                    'level': 'advanced',
                    'price': 369.00,
                    'duration_weeks': 14,
                    'instructor': 'Marcus Brown',
                    'max_students': 55,
                    'is_active': True,
                },
                {
                    'title': 'Blockchain Essentials',
                    'description': 'Understand distributed ledger technology, smart contracts, and blockchain use cases.',
                    'code': 'BCN100',
                    'level': 'intermediate',
                    'price': 289.00,
                    'duration_weeks': 10,
                    'instructor': 'Eva Laurent',
                    'max_students': 70,
                    'is_active': True,
                },
                {
                    'title': 'Project Management Certificate',
                    'description': 'Lead projects with agile methodology, stakeholder communication, and delivery discipline.',
                    'code': 'PMG110',
                    'level': 'beginner',
                    'price': 239.00,
                    'duration_weeks': 10,
                    'instructor': 'Daniel Kim',
                    'max_students': 90,
                    'is_active': True,
                },
                {
                    'title': 'Mobile App Development',
                    'description': 'Build modern mobile applications with React Native and cross-platform design patterns.',
                    'code': 'MOB210',
                    'level': 'intermediate',
                    'price': 279.00,
                    'duration_weeks': 10,
                    'instructor': 'Ravi Sharma',
                    'max_students': 80,
                    'is_active': True,
                },
                {
                    'title': 'Finance Analytics',
                    'description': 'Analyze financial datasets, forecast performance, and build investment dashboards.',
                    'code': 'FIN320',
                    'level': 'advanced',
                    'price': 349.00,
                    'duration_weeks': 12,
                    'instructor': 'Sophia Grant',
                    'max_students': 60,
                    'is_active': True,
                },
                {
                    'title': 'Creative Graphic Design',
                    'description': 'Design brand assets, digital campaigns, and visual identities using modern tools.',
                    'code': 'GRD430',
                    'level': 'beginner',
                    'price': 249.00,
                    'duration_weeks': 9,
                    'instructor': 'Carlos Vega',
                    'max_students': 75,
                    'is_active': True,
                },
                {
                    'title': 'Ethical Hacking Lab',
                    'description': 'Practice penetration testing and security analysis in a hands-on lab environment.',
                    'code': 'ETH501',
                    'level': 'advanced',
                    'price': 379.00,
                    'duration_weeks': 14,
                    'instructor': 'Mia Torres',
                    'max_students': 55,
                    'is_active': True,
                },
                {
                    'title': 'Kubernetes for Cloud Native Apps',
                    'description': 'Deploy, scale, and manage containerized applications with Kubernetes.',
                    'code': 'K8S620',
                    'level': 'intermediate',
                    'price': 329.00,
                    'duration_weeks': 12,
                    'instructor': 'Lena Wright',
                    'max_students': 70,
                    'is_active': True,
                },
                {
                    'title': 'Product Leadership and Strategy',
                    'description': 'Lead product teams, define roadmaps, and deliver customer-focused outcomes.',
                    'code': 'PLD710',
                    'level': 'advanced',
                    'price': 379.00,
                    'duration_weeks': 13,
                    'instructor': 'Noah Evans',
                    'max_students': 50,
                    'is_active': True,
                },
                {
                    'title': 'Visual Storytelling for Brands',
                    'description': 'Craft compelling brand narratives through design, copy, and digital media.',
                    'code': 'VSB830',
                    'level': 'beginner',
                    'price': 219.00,
                    'duration_weeks': 8,
                    'instructor': 'Isabella Ruiz',
                    'max_students': 85,
                    'is_active': True,
                },
                {
                    'title': 'SQL Analytics & Data Modeling',
                    'description': 'Analyze business data, build data models, and write powerful SQL queries.',
                    'code': 'SQL910',
                    'level': 'intermediate',
                    'price': 259.00,
                    'duration_weeks': 10,
                    'instructor': 'Tobias Reed',
                    'max_students': 75,
                    'is_active': True,
                },
                {
                    'title': 'Quantum Computing Fundamentals',
                    'description': 'Explore quantum computing principles, algorithms, and emerging applications.',
                    'code': 'QTM012',
                    'level': 'advanced',
                    'price': 429.00,
                    'duration_weeks': 16,
                    'instructor': 'Dr. Elena Park',
                    'max_students': 40,
                    'is_active': True,
                },
            ]

            existing_codes = set(Course.objects.values_list('code', flat=True))
            new_courses = [Course(**course) for course in default_courses if course['code'] not in existing_codes]
            if new_courses:
                Course.objects.bulk_create(new_courses)
        except (OperationalError, ProgrammingError):
            pass
        except Exception:
            pass
