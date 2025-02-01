from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.conf import settings
from user_agents import parse
from xauth. models import Activity
from django.utils import timezone

from educ_finance.decorators import admin_required, superuser_required

PUBLIC_NAMED_URLS = getattr(settings, "PUBLIC_NAMED_URLS", ())
ONLY_ADMINS_URLS = getattr(settings, "ONLY_ADMINS_URLS", ())
ONLY_SUPERUSER_URLS = getattr(settings, "ONLY_SUPERUSER_URLS", ())


class UserRightMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path_info).url_name

        decorator = None
        if url_name in ONLY_ADMINS_URLS:
            decorator = admin_required()
        if url_name in ONLY_SUPERUSER_URLS:
            decorator = superuser_required()
        else:
            return None

        return decorator(view_func)(request, *view_args, **view_kwargs)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path_info).url_name

        decorator = None
        if request.user.is_authenticated or (url_name in PUBLIC_NAMED_URLS):
            return None
        else:
            decorator = login_required()
            return decorator(view_func)(request, *view_args, **view_kwargs)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


from django.utils import timezone
from user_agents import parse

class ActivityMiddleware:
    def __init__(self, get_response):  # Corrige la syntaxe ici
        self.get_response = get_response

    def __call__(self, request):  # Corrige la syntaxe ici
        response = self.get_response(request)

        if request.user.is_authenticated:
            user_agent_str = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_str)
            os = user_agent.os.family if user_agent else 'Unknown'  # Gère le cas où `parse` échoue
            ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')  # Évite une erreur si absent

            action = f"Visited {request.path}"
            Activity.objects.create(
                user=request.user,
                action=action,
                timestamp=timezone.now(),
                ip_address=ip_address,
                user_agent=user_agent_str,
                os=os
            )

        return response
