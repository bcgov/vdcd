from rest_framework.authentication import TokenAuthentication
from keycloak import KeycloakOpenID
from api.models import AppUser, AppToken
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class KeycloakAuthentication(TokenAuthentication):
    keyword = "Bearer"

    # any valid idir token should authenticate the user successfully
    def authenticate_credentials(self, token):
        keycloak = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            realm_name=settings.KEYCLOAK_REALM,
        )
        KEYCLOAK_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\n"
            + keycloak.public_key()
            + "\n-----END PUBLIC KEY-----"
        )
        options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}

        try:
            token_info = keycloak.decode_token(
                token, key=KEYCLOAK_PUBLIC_KEY, options=options
            )
        except Exception:
            raise AuthenticationFailed("Invalid token")

        if token_info.get("identity_provider") == "idir":
            return AppUser.objects.get(app_name=settings.FRONTEND_APP_NAME), token

        raise AuthenticationFailed("Invalid token")


class CustomTokenAuthentication(TokenAuthentication):
    model = AppToken
