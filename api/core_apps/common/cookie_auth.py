from typing import Optional, Tuple
from django.conf import settings
from loguru import logger
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import Token

class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        raw_token = None
        if header is None:
            raw_token = self.get_raw_token(request)
        elif settings.COOKIE_NAME in request.cookies:
            raw_token = request.cookies[settings.COOKIE_NAME]
        
        if raw_token is not None:
            try:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token
            except TokenError as e:
                logger.error(f"Token error: {e}")
                raise InvalidToken(e) from e
            
        return None
    
    def get_header(self, request: Request) -> Optional[str]:
        header = request.headers.get(settings.COOKIE_NAME)
        if header is None:
            return None