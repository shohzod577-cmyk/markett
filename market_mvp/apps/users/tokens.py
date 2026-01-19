from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator for email verification."""


verification_token = EmailVerificationTokenGenerator()
