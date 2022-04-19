import os
import yadisk
# pip install yadisk

def upload_files(ynd_api, from_dir, to_dir):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from_dir = os.path.join(parent_dir, from_dir)
    docs_names = [file for file in os.listdir(from_dir)]
    
    try:
        ynd_api.mkdir(to_dir)
    except yadisk.exceptions.PathExistsError:
        pass
    
    for file in docs_names:
        file_path = os.path.join(from_dir, file)
        try:
            ynd_api.upload(file_path, to_dir + '/' + file)
        except yadisk.exceptions.PathExistsError:
            pass

if __name__ == '__main__':
    ynd_api = yadisk.YaDisk(token="AQAAAABf0mDbAAfRILWUrGyexE5BjRS_rtLyAWc")
    to_dir = "database"
    from_dir = "data_1"
    upload_files(ynd_api, from_dir, to_dir)