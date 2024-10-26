from rest_framework import serializers
from likes.models import Like
from django.conf import settings
from tweets.models import Tweet


class LikeModelSerializer(serializers.ModelSerializer):

    # Validates that the tweet is valid
    tweet = serializers.PrimaryKeyRelatedField(queryset=Tweet.objects.all())

    class Meta:
        model = Like
        fields = "__all__"
        read_only_fields = ("user",)  # The user field cannot be manually altered

    def create(self, validated_data):
        # The tweet is already being correctly passed in the JSON

        # Check if the authenticated user has already liked this tweet
        tweet = validated_data.get("tweet")
        user = self.context["request"].user

        # Check if the user has already liked the tweet
        if Like.objects.filter(user=user, tweet=tweet).exists():
            raise serializers.ValidationError("You have already liked this tweet.")

        # Automatically set the user as the authenticated user
        validated_data["user"] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        raise serializers.ValidationError("Editing a like is not allowed.")
