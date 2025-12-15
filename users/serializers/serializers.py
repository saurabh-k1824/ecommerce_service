import re
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=64,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "contact_number",
            "first_name",
            "last_name",
            "password",
            "role",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_active",  
            "created_at",
        ]

 

    def validate_email(self, value):
        value = value.strip().lower()

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
            raise serializers.ValidationError("Invalid email format.")

        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Email already registered.")

        return value

    def validate_contact_number(self, value):
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Contact number must contain digits only."
            )

        if not (10 <= len(value) <= 15):
            raise serializers.ValidationError(
                "Contact number must be between 10 and 15 digits."
            )

        qs = User.objects.filter(contact_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Contact number already registered.")

        return value

    def validate_password(self, value):
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        if re.search(r"\s", value):
            raise serializers.ValidationError(
                "Password must not contain spaces."
            )
        return value



    def validate(self, attrs):
        """
        Rules:
        - role is allowed ONLY during create
        - role cannot be modified during update
        - is_active cannot be modified via API
        """

        # UPDATE case
        if self.instance:
            if "role" in attrs:
                raise serializers.ValidationError(
                    {"role": "Role cannot be modified once assigned."}
                )

            if "is_active" in attrs:
                raise serializers.ValidationError(
                    {"is_active": "User activation/deactivation is not allowed via API."}
                )

        else:
            attrs.setdefault("role", "USER")

        return attrs


    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)  # 🔒 hashed
        user.save()

        return user



    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # 🔒 re-hash

        instance.save()
        return instance
