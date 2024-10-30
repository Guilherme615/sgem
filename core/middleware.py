# middleware.py

from django.contrib.auth.models import Group

class SidebarMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_groups = request.user.groups.values_list('name', flat=True)

            # Priorize a escolha da sidebar de acordo com o grupo do usuário
            if 'adm' in user_groups:
                request.sidebar_template = "includes/sidebar_adm.html"
            elif 'diretor' in user_groups:
                request.sidebar_template = "includes/sidebar_diretor.html"
            elif 'nutricionista' in user_groups:
                request.sidebar_template = "includes/sidebar_nutricionista.html"
            else:
                request.sidebar_template = "includes/sidebar03.html"
        else:
            request.sidebar_template = "includes/sidebar03.html"

        response = self.get_response(request)
        return response
