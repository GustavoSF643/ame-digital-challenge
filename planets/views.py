from django.http.response import HttpResponseNotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Planet
from .serializers import PlanetSerializer


class PlanetsView(APIView):
    def get(self, request):
        name = request.GET.get('name')
      
        planets = Planet.objects.all()

        if name:
            planets = planets.filter(name=name)

        serializer = PlanetSerializer(planets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        planet_data = request.data

        serializer = PlanetSerializer(data=planet_data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class PlanetsRetrieveView(APIView):
    def get(self, request, id):
        try:
            planet = Planet.objects.get(id=id)

            serializer = PlanetSerializer(planet)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Planet.DoesNotExist:
            return Response({"errors": "Planet not found."} ,status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            planet: Planet = Planet.objects.get(id=id)
            planet.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Planet.DoesNotExist:
            return Response({"errors": "Planet not found."} ,status=status.HTTP_404_NOT_FOUND)

        
