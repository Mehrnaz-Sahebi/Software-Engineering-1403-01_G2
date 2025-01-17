from rest_framework import serializers

class SuggestionSerializer(serializers.Serializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()
    suggest = serializers.CharField(max_length=255, trim_whitespace=False, allow_blank=True)

class TextSuggestionSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255, trim_whitespace=False)
