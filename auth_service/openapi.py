from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """
    OpenAPI schema definition for CustomJWTAuthentication
    """

    target_class = "auth_service.authentication.CustomJWTAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
