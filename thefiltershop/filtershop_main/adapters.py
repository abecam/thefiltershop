from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from django.conf import settings

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        If a user logs in with a social account and doesn't have a local account,
        create one and mark as pending approval.
        """
        user = sociallogin.user
        if not user.pk:
            # New user
            user.is_pending_approval = True  # Mark for admin approval
            user.save()

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.is_pending_approval = True
        user.save()
        return user