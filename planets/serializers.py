from rest_framework import serializers

from planets.models import Planet

class PlanetSerializer(serializers.Serializer):
    name = serializers.CharField()
    climate = serializers.CharField()
    terrain = serializers.CharField()
    movie_appearances = serializers.IntegerField()

    def create(self, validated_data):
        return Planet.objects.create(**validated_data)