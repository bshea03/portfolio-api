import os
from slowapi import Limiter
from slowapi.util import get_remote_address

APP_ENV = os.getenv("APP_ENV", "dev")
limiter = Limiter(key_func=get_remote_address)

class ProdLimiter(Limiter):
    def limit(self, *args, **kwargs):
        if APP_ENV == "prod":
            return super().limit(*args, **kwargs)
        else:
            # Return a no-op decorator
            def dummy_decorator(func):
                return func
            return dummy_decorator

limiter = ProdLimiter(key_func=get_remote_address)