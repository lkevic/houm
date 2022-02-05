from houmers.models import HoumerUser


class HoumerOAuth2TokenManager(object):
    @staticmethod
    def revoke_all_user_tokens(user: HoumerUser):
        if hasattr(user, 'oauth2_provider_accesstoken'):
            user.oauth2_provider_accesstoken.all().delete()
        if hasattr(user, 'oauth2_provider_refreshtoken'):
            user.oauth2_provider_refreshtoken.all().delete()
