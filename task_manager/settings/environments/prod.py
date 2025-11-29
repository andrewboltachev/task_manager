DEBUG = False

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True

# Uncomment when ready for https
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Email (e.g., SMTP or AWS SES)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# ... SMTP settings ...

STATIC_ROOT = BASE_DIR / "static"
