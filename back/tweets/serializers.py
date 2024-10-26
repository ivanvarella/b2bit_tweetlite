from rest_framework import serializers
from tweets.models import Tweet
import os
import uuid


class TweetModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False, allow_null=True, use_url=True
    )  # Allow image uploads via API

    class Meta:
        model = Tweet
        fields = "__all__"
        read_only_fields = ["author"]  # Prevents changing the author in update requests

    def _delete_old_image(self, instance):
        """Delete the old image file from storage if it exists."""
        if instance.image:
            if os.path.isfile(instance.image.path):
                try:
                    os.remove(instance.image.path)
                except (OSError, FileNotFoundError) as e:
                    print(f"Error deleting old image: {e}")

    def _rename_image(self, validated_data):
        """Renames the image if provided in the validated data."""
        if "image" in validated_data and validated_data["image"] is not None:
            image = validated_data["image"]
            # Validate image format
            if not image.name.lower().endswith((".png", ".jpg", ".jpeg")):
                raise serializers.ValidationError("Invalid image format.")

            # Always generate a new unique name for the image
            ext = os.path.splitext(image.name)[1]
            new_filename = f"{uuid.uuid4()}{ext}"
            image.name = new_filename
            return True
        return False

    # Overrides the `create` method to ensure that the author is the authenticated user when creating a new tweet
    def create(self, validated_data):
        # Set the author to the authenticated user
        validated_data["author"] = self.context["request"].user

        # Renames the image if provided
        if "image" in validated_data and validated_data["image"] is not None:
            self._rename_image(validated_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # If the request is PUT or PATCH, we ensure that the `author` is not modified
        request = self.context.get("request")

        # Prevent author changes
        if request.method == "PATCH" and "author" in validated_data:
            validated_data.pop("author")  # Removes the field if sent in PATCH
        elif request.method == "PUT" and "author" in validated_data:
            # Prevents changing the author in PUT but allows it to be present
            if validated_data.get("author") != instance.author:
                raise serializers.ValidationError(
                    {"author": "The author cannot be changed."}
                )

        # Manages the image if it is being updated
        if "image" in validated_data:
            # If setting it to None, just delete the old image
            if validated_data["image"] is None:
                self._delete_old_image(instance)
            else:
                # If sending a new image
                # 1. Delete the old one if it exists
                self._delete_old_image(instance)
                # 2. Rename the new image
                self._rename_image(validated_data)

        return super().update(instance, validated_data)
