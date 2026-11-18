from django.contrib.auth.models import User
from rest_framework import serializers

from tags.models import Tag

from .models import Category, Recipe


class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "author",
        ]

    public = serializers.BooleanField(source="is_published", read_only=True)
    preparation = serializers.SerializerMethodField(
        method_name="any_method_name", read_only=True
    )
    category = serializers.StringRelatedField()
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=65)
    # description = serializers.CharField(max_length=165)
    # public = serializers.BooleanField(source="is_published")
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all()
    # )
    # author= serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    tag_objects = TagSerializer(many=True, source="tags", read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source="tags",
        queryset=Tag.objects.all(),
        view_name="recipes:recipes_api_v2_tag",
    )

    def any_method_name(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    def validate(self, attrs):
        print()

# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ['id', 'title', 'description']
