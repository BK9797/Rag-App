from .BaseController import BaseController
from models.enums import ResponseEnum
from fastapi import UploadFile 
import os
import  re

class ProjectController(BaseController) :

    def __init__(self):
        super().__init__()

    def get_project_path(self , project_id :int) :
        project_dir = os.path.join(self.files_dir , str(project_id))

        if not os.path.exists(project_dir) :
            os.makedirs(project_dir)

        return project_dir

