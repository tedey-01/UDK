import os
import yadisk


TOKEN = "AQAAAABf0mDbAAfRILWUrGyexE5BjRS_rtLyAWc"


def upload_files_to_ynd(ynd_api: object, from_dir: str, to_dir: str):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    from_dir = os.path.join(parent_dir, from_dir)
    docs_names = [file for file in os.listdir(from_dir)]

    try:
        ynd_api.mkdir(to_dir)
    except yadisk.exceptions.PathExistsError:
        print(f'The folder {to_dir} already exists.')

    for file in docs_names:
        file_path = os.path.join(from_dir, file)
        try:
            ynd_api.upload(file_path, to_dir + '/' + file)
        except yadisk.exceptions.PathExistsError:
            print(f'The file {file} already exists.')


def download_files_from_ynd(ynd_api: object, from_dir: str, to_dir: str):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    to_dir = os.path.join(parent_dir, to_dir)
    docs_names = [file.name for file in ynd_api.listdir(from_dir)]
    docs_names = [d for d in docs_names if os.path.splitext(d)[-1] in ['.csv', '.joblib']]

    os.makedirs(to_dir, exist_ok=True)
    for filename in docs_names:
        src_file_path = os.path.join(from_dir, filename)
        loading_file_path = os.path.join(to_dir, filename)
        try:
            ynd_api.download(src_file_path, loading_file_path)
        except yadisk.exceptions.PathExistsError:
            print(f'The file {filename} not found.')


if __name__ == '__main__':
    ynd_api = yadisk.YaDisk(token=TOKEN)
    local_data_dir = "data"             ## ?? database ??
    ynd_data_dir = "database"           ## "udc_data"
    upload_files_to_ynd(ynd_api, local_data_dir, ynd_data_dir)
    download_files_from_ynd(ynd_api, ynd_data_dir, local_data_dir)
