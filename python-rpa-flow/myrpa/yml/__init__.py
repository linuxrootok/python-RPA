import os
PATH_YML = os.path.dirname(__file__)
#PATH_DATA_YML = os.path.dirname(__file__)+'/uploads'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"目录 {directory} 不存在，已创建")
    else:
        print(f"目录 {directory} 已存在")

def is_file_valid(file_path):
    if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
        return True
    else:
        return False
