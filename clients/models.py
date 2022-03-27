from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ClientManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, gender, password=None, **extra_fields):
        # Data validation
        if not email:
            raise ValueError('Clients must have the email address')
        if not username:
            raise ValueError('Clients must have the username')
        if not first_name:
            raise ValueError('Clients must have the first_name')
        if not last_name:
            raise ValueError('Clients must have the second_name')
        if not gender:
            raise ValueError('Clients must have gender')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, gender, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender
        )

        # Define superuser features
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Client(AbstractBaseUser):

    # Custom fields
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=True)

    class GenderChoices(models.IntegerChoices):
        MALE = 0
        FEMALE = 1

    gender = models.IntegerField(choices=GenderChoices.choices)
    avatar = models.ImageField(upload_to='clients/avatars', null=True, blank=True)

    objects = ClientManager()

    # Required fields for custom User model
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Auth configuration
    USERNAME_FIELD = 'email'  # Login field
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'gender')

    class Meta:
        app_label = 'clients'
        db_table = 'clients'
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        ordering = ('date_joined',)

    # Utility stuff
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True