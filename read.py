import boto3
import zipfile
import os
import re
from collections import defaultdict

# AWSの認証情報を設定
s3_client = boto3.client('s3')

def count_fail_pktversion(text):
    return text.count("fail pktversion")

def process_zip_files(bucket_name):
    # バケット内のすべてのZIPファイルをリストアップ
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    zip_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.zip')]

    # ZIPファイルごとに "fail pktversion" の出現回数をカウント
    date_fail_counts = defaultdict(int)
    file_pattern = re.compile(r'File_(\d{8}\d{2}).log')

    for zip_file_key in zip_files:
        # ZIPファイルをダウンロードして展開する
        zip_file_name = '/tmp/' + zip_file_key.split('/')[-1]
        s3_client.download_file(bucket_name, zip_file_key, zip_file_name)

        # ZIPファイルを展開
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall('/tmp/')

        # ファイルごとに "fail pktversion" の出現回数をカウント
        for root, _, files in os.walk('/tmp/'):
            for file_name in files:
                match = file_pattern.match(file_name)
                if match:
                    date = match.group(1)
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        contents = file.read()
                        fail_count = count_fail_pktversion(contents)
                        date_fail_counts[date] += fail_count

        # 一時ファイルを削除
        os.remove(zip_file_name)

    # カウント結果を出力
    for date, count in date_fail_counts.items():
        print(f"Date: {date}, Fail Count: {count}")

# メイン処理
if __name__ == "__main__":
    bucket_name = 'your-s3-bucket-name'  # S3バケット名

    process_zip_files(bucket_name)

