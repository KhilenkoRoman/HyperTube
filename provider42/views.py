import requests

from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import Provider42


class Provider42OAuth2Adapter(OAuth2Adapter):
    provider_id = Provider42.id

    access_token_url = 'https://api.intra.42.fr/oauth/token'
    authorize_url = 'https://api.intra.42.fr/oauth/authorize'
    profile_url = 'https://api.intra.42.fr/v2/me'

    # After successfully logging in, use access token to retrieve user info
    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url, params={'access_token': token.token})
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(Provider42OAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(Provider42OAuth2Adapter)


