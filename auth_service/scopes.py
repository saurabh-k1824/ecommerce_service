class Scopes:
    CATEGORIES_READ = "categories:read"
    CATEGORIES_WRITE = "categories:write"

    PRODUCTS_READ = "products:read"
    PRODUCTS_WRITE = "products:write"


    ORDERS_READ = "orders:read"
    ORDERS_WRITE = "orders:write"
    ORDERS_ADMIN = "orders:admin"

    USERS_READ = "users:read"
    USERS_WRITE = "users:write"


class ScopeService:
    ROLE_SCOPES = {
        "ADMIN": [
            Scopes.PRODUCTS_READ,
            Scopes.PRODUCTS_WRITE,
            Scopes.CATEGORIES_READ,
            Scopes.CATEGORIES_WRITE,
            Scopes.ORDERS_READ,
            Scopes.ORDERS_WRITE,
            Scopes.USERS_READ,
            Scopes.USERS_WRITE,
        ],
        "USER": [
            Scopes.PRODUCTS_READ,
            Scopes.CATEGORIES_READ,
            Scopes.ORDERS_READ,
            Scopes.ORDERS_WRITE,
        ],
    }

    @classmethod
    def scopes_for_role(cls, role: str) -> list[str]:
        return cls.ROLE_SCOPES.get(role, [])
