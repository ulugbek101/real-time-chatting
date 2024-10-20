from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager


class UserModelManager(UserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValidationError("Email is required")
        if "@" not in email:
            raise ValidationError("Email should contain '@' charachter")
        if not first_name:
            raise ValidationError("First name is required")
        if not last_name:
            raise ValidationError("Last name is required")
        email = self.normalize_email(email)
        username = email[:email.index("@")].lower()
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        superuser = self.create_user(email, first_name, last_name, password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)
        return superuser
