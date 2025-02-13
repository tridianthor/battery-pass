import os
from django.core.files.storage import FileSystemStorage

class Upload:
    #old method
    """ @classmethod
    def handle_upload(self, path, uploaded_file):
        with open(f'{path}/{uploaded_file.name}', 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk) """
    @classmethod
    def handle_single_upload(self, path, file, intended_filename):
        print(f'{path}, {file.name}, {intended_filename}')
        private_storage = FileSystemStorage(location=path)
        extension = self.get_file_extension(file.name)
        uploaded_file = private_storage.save(f'{intended_filename}{extension}', file)
        return uploaded_file
    
    @classmethod
    def get_file_extension(self, filename):
        file_name, file_extension = os.path.splitext(filename)
        return file_extension