from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    address_line1 = models.CharField(max_length=255, default='N/A')
    city = models.CharField(max_length=100, default='N/A')
    state = models.CharField(max_length=100, default='N/A')
    pincode = models.CharField(max_length=10, default='000000')
    
    def __str__(self):
        return f"{self.user.username} Profile"
