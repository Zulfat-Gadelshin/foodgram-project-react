from base64 import b64decode
from django.core.files.base import ContentFile
from imghdr import what
from rest_framework.serializers import ImageField
from six import string_types
from uuid import uuid4


class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, string_types):
            if "data:" in data and ";base64," in data:
                header, data = data.split(";base64,")
            try:
                decoded_file = b64decode(data)
            except TypeError:
                self.fail("Изображение не соответствует")
            file_name = str(uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension)
            data = ContentFile(decoded_file, name=complete_file_name)
        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = what(file_name, decoded_file)
        return "jpg" if extension == "jpeg" else extension
