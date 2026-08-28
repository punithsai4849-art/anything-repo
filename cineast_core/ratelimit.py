import time
from django.core.cache import cache
from django.http import HttpRequest

def get_client_ip(request: HttpRequest) -> str:
    """
    Safely extract client IP address using REMOTE_ADDR.
    Do not trust arbitrary X-Forwarded-For headers to prevent spoofing.
    """
    return request.META.get('REMOTE_ADDR', '127.0.0.1')

def check_rate_limit(request: HttpRequest, action: str, max_attempts: int = 10, timeout: int = 900) -> bool:
    """
    Check if the client has exceeded the maximum allowed attempts for a given action.
    Returns True if rate limited (blocked), False if request is allowed.
    """
    ip = get_client_ip(request)
    cache_key = f"rl:{action}:{ip}"
    
    attempts = cache.get(cache_key, 0)
    if attempts >= max_attempts:
        return True
    
    return False

def record_rate_limit_attempt(request: HttpRequest, action: str, timeout: int = 900) -> int:
    """
    Increment the rate limit attempt counter for the client IP.
    """
    ip = get_client_ip(request)
    cache_key = f"rl:{action}:{ip}"
    
    try:
        attempts = cache.get(cache_key, 0)
        if attempts == 0:
            cache.set(cache_key, 1, timeout)
            return 1
        else:
            return cache.incr(cache_key)
    except Exception:
        # Fallback if cache doesn't support incr
        attempts = cache.get(cache_key, 0) + 1
        cache.set(cache_key, attempts, timeout)
        return attempts

def reset_rate_limit(request: HttpRequest, action: str):
    """
    Reset the rate limit counter (e.g. upon successful authentication).
    """
    ip = get_client_ip(request)
    cache_key = f"rl:{action}:{ip}"
    cache.delete(cache_key)
