import os
import yadisk
# pip install yadisk

def upload_files(y, from_dir, to_dir):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from_dir = os.path.join(parent_dir, from_dir)
    docs_names = [file for file in os.listdir(from_dir)]
    
    try:
        y.mkdir(to_dir)
    except yadisk.exceptions.PathExistsError:
        pass
    
    for i, file in enumerate(docs_names):
        file_path = os.path.join(from_dir, file)
        print(i ,'/',len(docs_names), file_path)
        try:
            i += 1
            y.upload(file_path, to_dir + '/' + file)
        except yadisk.exceptions.PathExistsError:
            pass

if __name__ == '__main__':
    y = yadisk.YaDisk(token="AQAAAABf0mDbAAfRILWUrGyexE5BjRS_rtLyAWc")
    to_dir = "database"
    from_dir = "data_1"
    upload_files(y, from_dir, to_dir)