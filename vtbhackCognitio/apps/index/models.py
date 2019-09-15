from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Document(models.Model):
    user_id = models.ManyToManyField(User)
    title = models.CharField('Title', max_length=200)
    text = models.TextField('Text')
    is_active = models.BooleanField('Active', default=True)
    end_date = models.DateTimeField('End date')

class DocumentFile(models.Model):
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    file_path = models.FilePathField('Path to file')

class Comment(models.Model):
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Text')
    date = models.DateTimeField('Publishment date')
    

class Result(models.Model):
    YES = 1
    NO = 0
    NO_RESULT = 2
    RESULTS = [
        (YES, 'Yes'),
        (NO, 'No'),
        (NO_RESULT, 'No result')
    ]
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.IntegerField('Result', choices=RESULTS, default=NO_RESULT)
    date = models.DateTimeField('Date of update', auto_now_add=True)