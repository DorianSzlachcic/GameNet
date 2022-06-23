from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

def check_if_redactor(user):
    if user.groups.filter(name='redactor').exists():
        return True
    else:
        raise PermissionDenied
