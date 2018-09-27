from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class Provider42Account(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get('url')

    def get_avatar_url(self):
        return self.account.extra_data.get('image_url')

    def to_str(self):
        dflt = super(Provider42Account, self).to_str()
        return self.account.extra_data.get('login', dflt)


class Provider42(OAuth2Provider):
    id = "provider42"
    name = "Provider42"
    account_class = Provider42Account

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(email=data.get('email'),
                    last_name=data.get('last_name'),
                    first_name=data.get('first_name'))

    # with email get
    # def extract_common_fields(self, data):
    #     return dict(email=data.get('email'),
    #                 last_name=data.get('last_name'),
    #                 first_name=data.get('first_name'))


provider_classes = [Provider42]
