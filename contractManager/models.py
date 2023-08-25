from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    SALES = 'Sales'
    MANAGEMENT = 'Management'
    SUPPORT = 'Support'
    # Add script to create roles
    ROLE_CHOICES = [
        (SALES, 'Sales'),
        (MANAGEMENT, 'Management'),
        (SUPPORT, 'Support'),
    ]

    name = models.CharField(max_length=255, choices=ROLE_CHOICES)

    def __str__(self):
        return self.get_name_display()  # This will return the display value for the selected choice (e.g., 'Sales', 'Management', 'Support')


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255)
    creation_date = models.DateTimeField()
    last_contact_date = models.DateTimeField()
    sales_contact = models.ForeignKey(
        CustomUser, related_name="clients", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        
    def __str__(self):
        return f"client: {self.full_name} - company: {self.company_name}"


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sales_contact = models.ForeignKey(
        CustomUser, related_name="contracts", on_delete=models.CASCADE
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField()
    is_signed = models.BooleanField()

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        
    def __str__(self):
        return f"Contract: '{self.is_signed}' for 'client: {self.client}'"


class Event(models.Model):
    event_id = models.CharField(max_length=255)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    client_contact = models.CharField(max_length=255)
    event_date_start = models.DateTimeField()
    event_date_end = models.DateTimeField()
    support_contact = models.ForeignKey(
        CustomUser,
        related_name="supported_events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=255)
    attendees = models.IntegerField()
    notes = models.TextField()

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        
    def __str__(self):
        return f"Event: {self.event_id} Contract: '{self.contract}' for 'client: {self.client_name}'"
