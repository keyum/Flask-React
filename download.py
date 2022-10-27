import os
from multiprocessing import Process
from zipfile import ZipFile

import requests

extract_dir = "./xmls/"
download_dir = "./downloads/"


class Downloader():

    def download_file(self, url):
        file_name = url.split("/")[-1]
        try:
            response = requests.get(url)
            # sub_dir = Path(download_dir)
            # sub_dir.mkdir(parents=True, exist_ok=True)
            with open(f"{download_dir}{file_name}", "wb") as f:
                f.write(response.content)
            return file_name
        except Exception as e:
            print(f"Error {e} occurred during downloading from {url}")

    def extract_file(self, zip_file):
        with ZipFile(zip_file, 'r') as zf:
            zf.extractall(f"{extract_dir}{zip_file.split('.')[0]}/")

    def parallel_running(self, target, file_names):
        processes = []
        for file_name in file_names:
            p = Process(target=target, args=(file_name,))
            p.start()
            processes.append(p)
        for process in processes:
            process.join()


def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.mkdir(download_dir)


if __name__ == "__main__":
    urls = []
    file_names = []

    create_directory(download_dir)
    create_directory(extract_dir)

    # download csv and zip files
    csv_url = "https://ms-codechallenge.s3.amazonaws.com/index_2020.csv"
    downloader = Downloader()
    downloader.download_file(csv_url)

    # download zip files in parallel
    for i in range(1, 9):
        url = f"https://ms-codechallenge.s3.amazonaws.com/download990xml_2020_{i}.zip"
        name = url.split("/")[-1]
        urls.append(url)
        file_names.append(name)
    downloader.parallel_running(downloader.download_file, urls)  # Do NOT use parallel_running if the files are too big
    # unzipping xmls in parallel
    downloader.parallel_running(downloader.extract_file, file_names)
