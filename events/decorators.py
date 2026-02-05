from django.contrib.auth.decorators import user_passes_test

def admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'userprofile') and u.userprofile.role == 'ADMIN',
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def organizer_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'userprofile') and u.userprofile.role == 'ORGANIZER',
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def organizer_or_admin_required(function=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'userprofile') and u.userprofile.role in ['ORGANIZER', 'ADMIN'],
        login_url='login',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
