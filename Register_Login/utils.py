from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone

class AccessTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp): 
        return f'{user.email}{timestamp}{user.is_active}'