from zipfile import ZipFile


# def read_zip_file(file_path: str | Path):
def read_zip_file(file_path: str):
    news_zip_path = file_path
    with ZipFile(news_zip_path, 'r') as zip:
        return zip.read()

# news_zip_path = read_zip_file(file_path="articles-validation-bypublisher-20181122.xml")
# ground_truth_zip_path = read_zip_file(file_path="ground-truth-validation-bypublisher-20181122.xml")
