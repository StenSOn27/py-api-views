from rest_framework import serializers
from .models import Actor, Movie, CinemaHall, Genre


class ActorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.save()
        return instance


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class CinemaHallSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    rows = serializers.IntegerField()
    seats_in_row = serializers.IntegerField()

    def create(self, validated_data):
        return CinemaHall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.rows = validated_data.get("rows", instance.rows)
        instance.seats_in_row = validated_data.get(
            "seats_in_row", instance.seats_in_row
        )
        instance.save()
        return instance


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    duration = serializers.IntegerField()
    genres = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )
    actors = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    def create(self, validated_data):
        genres_data = validated_data.pop("genres", [])
        actors_data = validated_data.pop("actors", [])
        movie = Movie.objects.create(**validated_data)
        movie.genres.set(Genre.objects.filter(id__in=genres_data))
        movie.actors.set(Actor.objects.filter(id__in=actors_data))
        return movie

    def update(self, instance, validated_data):
        genres_data = validated_data.pop("genres", None)
        actors_data = validated_data.pop("actors", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if genres_data is not None:
            instance.genres.set(Genre.objects.filter(id__in=genres_data))
        if actors_data is not None:
            instance.actors.set(Actor.objects.filter(id__in=actors_data))

        instance.save()

        return instance
