from django.conf import settings

class SecurityHeadersMiddleware:
    """
    Global security headers middleware applying strict CSP, Referrer-Policy,
    MIME sniffing protection, and HSTS.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content-Security-Policy
        csp_directives = [
            "default-src 'self'",
            "img-src 'self' data: https: blob:",
            "style-src 'self' 'unsafe-inline'",
            "script-src 'self' 'unsafe-inline'",
            "font-src 'self' data:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response.headers['Content-Security-Policy'] = "; ".join(csp_directives)

        # Referrer-Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # X-Content-Type-Options & X-Frame-Options
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'

        # Strict-Transport-Security in production
        if not settings.DEBUG:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        return response
