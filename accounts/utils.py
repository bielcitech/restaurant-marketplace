from django.core.exceptions import PermissionDenied

def detect_user(user):
    if user.is_vendor:
        return "dashboard"
    return "my-account"


def customer_access(user):
    if user.is_vendor:
        raise PermissionDenied
    return True


def vendor_access(user):
    if user.is_vendor:
        return True
    raise PermissionDenied