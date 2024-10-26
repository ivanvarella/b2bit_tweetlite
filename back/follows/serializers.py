from rest_framework import serializers
from follows.models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the AUTH_USER_MODEL


class FollowModelSerializer(serializers.ModelSerializer):

    # Validates that the following user is a valid user
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ("follower",)  # Read-only, does not allow changes

    def create(self, validated_data):
        # The "following" is already being passed correctly in the JSON

        # Checks if the user is trying to follow themselves
        following_user = validated_data.get("following")
        if following_user == self.context["request"].user:
            raise serializers.ValidationError("You cannot follow yourself.")

        # Checks if the (authenticated) user is already following this following user
        follower_user = self.context["request"].user
        if Follow.objects.filter(
            follower=follower_user, following=following_user
        ).exists():
            raise serializers.ValidationError("You are already following this user.")

        # Automatically set the follower as the authenticated user
        validated_data["follower"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Editing a follow is not allowed.")
