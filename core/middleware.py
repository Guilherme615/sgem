from django.contrib.auth.models import Group
from django.utils.deprecation import MiddlewareMixin

class SidebarMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define o template da sidebar de acordo com o grupo do usuário
        if request.user.is_authenticated:
            user_groups = request.user.groups.values_list('name', flat=True)
            # Verifique os grupos e defina o template correspondente
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

        # Debug: Verifique o valor de request.sidebar_template
        print(f'Sidebar template: {request.sidebar_template}')
