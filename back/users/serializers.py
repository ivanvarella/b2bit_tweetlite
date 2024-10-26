from rest_framework import serializers
from users.models import CustomUser
import os
import uuid


class CustomUserModelSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        required=False, allow_null=True, use_url=True
    )  # Allow image uploads via API
    # The parameter "use_url=True" allows the full URL of the image to be returned instead of the file path.

    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate(self, data):
        # Checks if 'is_superuser' or 'is_staff' are being set to True
        if data.get("is_superuser") or data.get("is_staff"):
            raise serializers.ValidationError(
                "You cannot create a superuser or staff user via this endpoint."
            )
        return data

    def _delete_old_image(self, instance):
        """Delete the old image file from storage if it exists."""
        if instance.profile_picture:
            if os.path.isfile(instance.profile_picture.path):
                try:
                    os.remove(instance.profile_picture.path)
                except (OSError, FileNotFoundError) as e:
                    print(f"Error deleting old image: {e}")

    def _rename_image(self, validated_data):
        """Renames the profile picture if provided in the validated data."""
        if (
            "profile_picture" in validated_data
            and validated_data["profile_picture"] is not None
        ):
            image = validated_data["profile_picture"]
            # Validate image format
            if not image.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise serializers.ValidationError("Invalid image format.")

            # Always generate a new unique name for the image
            ext = os.path.splitext(image.name)[1]  # Gets the file extension
            new_filename = f"{uuid.uuid4()}{ext}"  # Creates a new file name
            image.name = new_filename  # Renames the image
            return True
        return False

    def create(self, validated_data):
        # Ensures that is_staff and is_superuser are always False
        validated_data["is_staff"] = False
        validated_data["is_superuser"] = False

        # Renames the profile picture if provided
        if (
            "profile_picture" in validated_data
            and validated_data["profile_picture"] is not None
        ):
            self._rename_image(validated_data)

        # Creates the user
        user = CustomUser(**validated_data)
        user.set_password(
            validated_data["password"]
        )  # Encrypts the password before saving
        user.save()
        return user

    def update(self, instance, validated_data):

        # Checks if the password was provided in the update payload
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)  # Encrypts the new password

        # Manages the profile picture if it is being updated
        if "profile_picture" in validated_data:
            # If setting it to None, just delete the old image
            if validated_data["profile_picture"] is None:
                self._delete_old_image(instance)
            else:
                # If sending a new image
                # 1. Delete the old one if it exists
                self._delete_old_image(instance)
                # 2. Rename the new image
                self._rename_image(validated_data)

        # Updates the remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()  # Saves the changes to the database
        return instance
