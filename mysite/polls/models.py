from django.db import models #type: ignore

# Create your models here.

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=30, unique=True)
    contact_email = models.EmailField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    eir_code = models.CharField(max_length=7, blank=True)

    def __str__(self):
        return self.company_name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Campaign(models.Model):
    STATUS_CHOICES = [
        ('PL', 'Planning'),
        ('IP', 'In Progress'),
        ('CR', 'Client Review'),
        ('OH', 'On Hold'),
        ('CP', 'Completed'),
    ]

    campaign_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30) 
    description = models.TextField(blank=True) 
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    campaign_manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_projects')
    start_date = models.DateField(null=True, blank=True) 
    completion_date = models.DateField(null=True, blank=True) 
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.client.company_name})"

class Task(models.Model):
    STATUS_CHOICES = [
        ('TD', 'To Do'),
        ('IP', 'In Progress'),
        ('CR', 'Client Review'),
        ('DN', 'Done'),
    ]

    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=30) 
    description = models.TextField(blank=True) 
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks') 
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='TD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Project: {self.project.name})"

class Deliverable(models.Model):
    STATUS_CHOICES = [
        ('WIP', 'Work In Progress'),
        ('PCA', 'Pending Client Approval'),
        ('APRV', 'Approved'),
    ]

    deliverable_id = models.AutoField(primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='deliverables')
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"