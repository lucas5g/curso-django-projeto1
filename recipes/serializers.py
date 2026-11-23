from django.contrib.auth.models import User
from rest_framework import serializers
from tags.models import Tag
from .models import Category, Recipe
from authors.validators import AuthorRecipeValidator

class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]

    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "description",
            "author",
            "public",
            "preparation_time",
            "preparation",
            "servings",
            "servings_unit",
            "category",
            "tags",
            "tag_objects",
            "tag_links",
            "cover"

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
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    tag_objects = TagSerializer(many=True, source="tags", read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source="tags",
        queryset=Tag.objects.all(),
        view_name="recipes:recipes_api_v2_tag",
        required=False
    )

    def any_method_name(self, recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    def validate(self, attrs):

        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings 

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs, ErrorClass=serializers.ValidationError
        )
        return super_validate
