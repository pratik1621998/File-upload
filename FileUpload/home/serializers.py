from rest_framework import serializers
from .models import *
import shutil


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Files
        fields = '__all__'


class FileListSerializer(serializers.Serializer):
    
    files = serializers.ListField(
        child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False)
    )
    folder = serializers.CharField(required = False)

    def zip_file(self, folder):
        shutil.make_archive(f"public/static/zip/{folder}", 'zip', f"public/static/{folder}")


    def create(self, validated_data):
        folder = Folder.objects.create()
        files = validated_data.pop('files')
        files_objs = []
        for file in  files:
            file_obj = Files.objects.create(folder= folder, file = file)
            files_objs.append(file_obj)

        self.zip_file(folder.uid)

        return {'files' : {} , 'folder' : str(folder.uid)}