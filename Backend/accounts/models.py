from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_mobile_no(instance):
    if len(instance) != 10:
        raise ValidationError("Invalid Mobile Number")
    return instance


class UserType(models.Choices):
    DISCORD = "Discord"
    WEBCHAT = "web Chat"
    WEBSITE = "Website"
    TELEGRAM = "Telegram"
    OTHERS = "Other"

class User(models.Model):
    mobile_no = models.IntegerField(unique=True, editable=False, validators=[validate_mobile_no])
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    usertype = models.CharField(choices=UserType.choices, max_length=15)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.mobile_no
