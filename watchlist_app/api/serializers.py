from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Reviews

class ReviewSerializer(serializers.ModelSerializer):
    watchlist_name = serializers.SlugRelatedField(slug_field='title', read_only=True, source='watchlist')
    watchlist_url = serializers.HyperlinkedRelatedField(
        view_name='movie-detail',  # The name of the watchlist detail view
        lookup_field='pk',             # How the URL will look up the watchlist
        read_only=True,
        source='watchlist'             # This links the URL to the watchlist ForeignKey in the Review model
    )
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        fields = "__all__"
        # exclude = ('watchlist',)
        # include = ('watchlist_name',)
        # fields = '__all__'

class WatchListSerializer(serializers.ModelSerializer):

    # len_name = serializers.SerializerMethodField() #Creates a custom field for the serializer which is not in views/model
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"
        # include = ('watchlist_name',)
        # fields = ['id', 'name', 'description'] Will display only the fields mentioned inside list
        # exclude = ['description'] Will not display fields displayed inside the list


class StreamPlatformSerializer(serializers.ModelSerializer):
    #watchlist = WatchListSerializer(many=True, read_only=True) # the variable name(here watchlist) should be same as the one set in related_name="var" in models
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"


    # def get_len_name(self, object):
    #     return len(object.name)

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and description should be different.")
    #     return data

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     return value

# def name_length(value):
#     if len(value) < 2:
#             raise serializers.ValidationError("Name is too short")
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.description = validated_data.get("description", instance.description)
#         instance.active = validated_data.get("active", instance.active)
#         instance.save()
#         return instance

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and description should be different.")
#         return data

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
    #     return value