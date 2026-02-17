from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
from fastapi import UploadFile 
import re
import os

class DataController (BaseController) :
    
    def __init__(self):
        super().__init__() # to get copy of app_setting that is created in BaseController

        self.size_scale = 1048576 # convert MB to bytes
    
    def validate_uploaded_file(self , file : UploadFile ):

        if file.content_type not in self.app_setting.FILE_ALLOWED_TYPES :
            return False ,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_setting.FILE_MAX_SIZE * self.size_scale :
            return False , ResponseSignal.FILE_SIZE_TOO_LARGE.value
        
        return True , ResponseSignal.FILE_UPLOAD_SUCCESS.value
    
    def generate_unique_filepath (self ,orig_file_name :str , project_id : str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        clean_file_name =self.get_clean_file_name(orig_file_name)

        new_file_path = os.path.join(project_path, f"{random_key}_{clean_file_name}")

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_key}_{clean_file_name}")

        
        return new_file_path , random_key + "_" + clean_file_name 


    
    def get_clean_file_name (self ,orig_file_name :str):
        clean_file_name =re.sub(r'[^\w.]' , '',orig_file_name.strip())

        clean_file_name = clean_file_name.replace(" " ,"_")

        return clean_file_name



