from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

def check_if_reviewer(user):
    if user.groups.filter(name='reviewer').exists():
        return True
    else:
        raise PermissionDenied
