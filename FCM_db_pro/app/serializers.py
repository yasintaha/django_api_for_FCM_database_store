from rest_framework import serializers

class ReportSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=143)
    password = serializers.CharField(max_length=143)
    work_assigned = serializers.CharField(max_length=243)
    progress = serializers.CharField(max_length=243)
