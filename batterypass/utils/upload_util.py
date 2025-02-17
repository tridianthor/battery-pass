from utils.resp import Resp
from django.core.files.storage import FileSystemStorage

import os

class Upload:
    #old method
    """ @classmethod
    def handle_upload(self, path, uploaded_file):
        with open(f'{path}/{uploaded_file.name}', 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk) """
    @classmethod
    def handle_single_upload(self, path, file, intended_filename):
        private_storage = FileSystemStorage(location=path)
        extension = self.get_file_extension(file.name)
        uploaded_file = private_storage.save(f'{intended_filename}{extension}', file)
        return uploaded_file
    
    @classmethod
    def get_file_extension(self, filename):
        file_name, file_extension = os.path.splitext(filename)
        return file_extension
    
    @classmethod
    def check_exist(self, filepath):
        fs = FileSystemStorage()
        print(f'file {filepath} exist : {fs.exists(filepath)}')
        return fs.exists(filepath)
    
    @classmethod
    def remove_to_replace(self, filepaths):
        try:
            for filepath in filepaths:
                print(f'file to remove : {filepath}')
                os.remove(filepath)
            return Resp(True, "File removed")
        except Exception as exception:
            return Resp(False, exception)