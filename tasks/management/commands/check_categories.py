from django.core.management.base import BaseCommand
from tasks.models import TaskCategory

class Command(BaseCommand):
    help = 'Check and create default task categories if they don\'t exist'

    def handle(self, *args, **options):
        default_categories = [
            {
                'name': 'Development',
                'description': 'Software development tasks',
                'color': '#007bff'
            },
            {
                'name': 'Design',
                'description': 'UI/UX design tasks',
                'color': '#28a745'
            },
            {
                'name': 'Testing',
                'description': 'Quality assurance and testing tasks',
                'color': '#ffc107'
            },
            {
                'name': 'Documentation',
                'description': 'Documentation and writing tasks',
                'color': '#6c757d'
            },
            {
                'name': 'Research',
                'description': 'Research and analysis tasks',
                'color': '#17a2b8'
            }
        ]

        created_count = 0
        for category_data in default_categories:
            category, created = TaskCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'color': category_data['color']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Total categories: {TaskCategory.objects.count()}')
        ) 