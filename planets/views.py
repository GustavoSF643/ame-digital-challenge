import django
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
        try:
            planet_data = request.data

            def get_planet(url, planet_name):
                import requests
                import json

                planets = requests.get(url)
                planets_content = json.loads(planets.content)

                planet = filter(lambda x: [y for y in x if x['name'] == planet_name], planets_content["results"])
                planet_list = list(planet)
                
                if not planet_list and planets_content['next']:
                    return get_planet(planets_content['next'], planet_name)

                if len(planet_list) > 0:
                    return planet_list[0]


            planet = get_planet('https://swapi.dev/api/planets', planet_data['name'])

            if not planet:
                return Response({"erros": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

            planet_data['movie_appearances'] = len(planet['films'])

            serializer = PlanetSerializer(data=planet_data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        except django.db.utils.IntegrityError:
            return Response({"erros": "Planet already registered."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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

        
