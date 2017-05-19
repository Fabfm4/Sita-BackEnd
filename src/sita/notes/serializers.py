from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.Serializer):
    """"""
    title = serializers.CharField(
        required = True,
        max_length = 100
    )
    content = serializers.CharField(
        min_length=20,
        required=True
    )

class NoteSerializerModel(serializers.ModelSerializer):
    """
    Serializer used to return the proper token, when the user was succesfully
    logged in.
    """

    class Meta:
        model = Note
        fields = ('id',
                'title',
                'content',
                'created_date',)
