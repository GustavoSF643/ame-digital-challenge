from rest_framework import serializers

class PlanetSerializer(serializers.Serializer):
    name = serializers.CharField()
    climate = serializers.CharField()
    terrain = serializers.CharField()
    movie_appearances = serializers.IntegerField()