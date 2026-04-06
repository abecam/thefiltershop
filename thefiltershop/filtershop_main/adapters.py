from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.conf import settings

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        If a user logs in with a social account and doesn't have a local account,
        create one and give them staff access if they are the first user or something.
        For simplicity, let's give all social logins staff access (in production, restrict this).
        """
        user = sociallogin.user
        if not user.pk:
            # New user
            user.is_staff = True  # Allow admin access
            user.is_superuser = False  # Not superuser by default
            user.save()

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_staff = True
        user.save()
        return user