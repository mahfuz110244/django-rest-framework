import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin
)
from api.core.models import TimestampedModel
from django.db import models
from django.utils import timezone



# Create your models here.

class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username, email, password, contact_id=None,
                    security_question=None, security_answer=None,
                    status=None, terms_and_condition_accepted=None,
                    created_uid=None, updated_uid=None):
        """Create and return a `User` with an email, username and password."""
        # username = data['username']
        # email = data['email']
        # password = data['password']
        # contact_id = data['contact_id']
        # security_question = data.get('security_question','')
        # security_answer = data.get('security_answer','')
        # status = data['status']
        # terms_and_condition_accepted = data['terms_and_condition_accepted']
        # created_uid = data['created_uid']
        # updated_uid = data['updated_uid']

        user = self.model(username=username,
                          email=self.normalize_email(email),
                          contact_id = contact_id,
                          security_question = (security_question,''),
                          security_answer = (security_answer,''),
                          status = status,
                          terms_and_condition_accepted = terms_and_condition_accepted,
                          created_uid=created_uid,
                          updated_uid=updated_uid
                          )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, contact_id=None,
                    security_question=None, security_answer=None,
                    status=None, terms_and_condition_accepted=None,
                    created_uid=None, updated_uid=None):
      """
      Create and return a `User` with superuser powers.

      Superuser powers means that this use is an admin that can do anything
      they want.
      """
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.create_user(username, email, password,status=True,terms_and_condition_accepted=True)
      user.is_superuser = True
      user.is_staff = True
      user.status = True
      user.terms_and_condition_accepted = True
      user.save()

      return user


# Create your models here.
class Contacts(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.CharField(max_length=10,blank=True)
    estimated_age = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False, blank=True)
    revera_id = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=50,blank=True)
    national_id = models.CharField(max_length=50,blank=True)
    medical_insurance_id = models.CharField(max_length=50,blank=True)
    ethnicity = models.CharField(max_length=50,blank=True)
    religion = models.CharField(max_length=20,blank=True)
    merital_status = models.CharField(max_length=20,blank=True)
    blood_group = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=50, blank=True, unique=True)
    username = models.CharField(max_length=50, blank=True, unique=True)
    phone = models.CharField(max_length=50,blank=True)
    height = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=20, blank=True)
    alergies = models.TextField(max_length=500, blank=True)
    profile_photo = models.ImageField(upload_to='images', max_length=254, blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_uid = models.ForeignKey('User', related_name='user1', blank=True, null=True)
    updated_date = models.DateTimeField(default=timezone.now)
    updated_uid = models.ForeignKey('User', related_name='user2', blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):  # __unicode__ on Python 2
        return self.first_name + " " + self.last_name

class ContactsAttributes(models.Model):
    contact_id = models.ForeignKey(Contacts, on_delete=models.CASCADE, blank=True, null=True)
    attribute_key = models.CharField(max_length=50, blank=True)
    attribute_value = models.TextField(max_length=500, blank=True)

    created_date = models.DateTimeField(default=timezone.now)
    created_uid = models.ForeignKey('User', related_name='user3', blank=True, null=True)
    updated_date = models.DateTimeField(default=timezone.now)
    updated_uid = models.ForeignKey('User', related_name='user4', blank=True, null=True)


class User(AbstractUser, TimestampedModel):
    # # Each `User` needs a human-readable unique identifier that we can use to
    # # represent the `User` in the UI. We want to index this column in the
    # # database to improve lookup performance.
    # username = models.CharField(db_index=True, max_length=255, unique=True)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True)
    contact_id = models.ForeignKey(Contacts, on_delete=models.CASCADE, blank=True, null=True)
    security_question = models.TextField(max_length=500, blank=True, default="")
    security_answer = models.TextField(max_length=500, blank=True,default="")
    status = models.BooleanField(default=False, blank=True)
    terms_and_condition_accepted = models.BooleanField(default=False, blank=True)

    # When a user no longer wishes to use our platform, they may try to delete
    # there account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. To solve this problem, we
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    # is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users, this flag will always be
    # falsed.
    # is_staff = models.BooleanField(default=False)

    # name = models.CharField(max_length=50, blank=True)

    # More fields required by Django when specifying a custom user model.

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case, we want that to be the email field.
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
      """
      This method is required by Django for things like handling emails.
      Typically, this would be the user's first and last name. Since we do
      not store the user's real name, we return their username instead.
      """
      return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(hours=1)

        token = jwt.encode({
            'username': self.username,
            'password': self.password,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)


