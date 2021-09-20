from wtforms.csrf.core import CSRF
from utils.tokens.token_manager import BaseTokenManager


class RedisCacheCSRF(CSRF):
    """
    Generate a CSRF token for form using a token provider based on storing CSRF tokens in a redis
    key-value store
    """
    def setup_form(self, form):
        # Check that the token manager exists and is a TokenManager
        assert(isinstance(form.meta.csrf_token_mgr, BaseTokenManager))
    
        self.csrf_token_mgr = form.meta.csrf_token_mgr
        self.session = form.meta.session

        return super(RedisCacheCSRF, self).setup_form(form)


    def generate_csrf_token(self, csrf_token_field):
        if self.session == None: 
            return self.csrf_token_mgr.create_sessionless_csrf_token()
        else: 
            return self.session.csrf_token


    def validate_csrf_token(self, form, field):
        token = field.data
        if self.session == None: 
            is_valid = self.csrf_token_mgr.is_valid_sessionless_csrf(token)
        else: 
            is_valid = self.csrf_token_mgr.validate_csrf_session_token(
                token, 
                self.session 
            )

        if not is_valid:
            raise ValueError('Invalid CSRF Token')
