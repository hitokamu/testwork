import os
import gzip
import boto3
import re

# AWS S3の設定
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
s3_bucket_name = 'YOUR_S3_BUCKET_NAME'
s3_prefix = 'path/to/logs/'  # ファイルの格納パスを指定
file_pattern = r'\d{10}\.log\.gz'  # ファイル名の正規表現パターン

# S3クライアントの作成
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def download_and_process_file(filename):
    # S3からファイルをダウンロード
    s3_object = s3.get_object(Bucket=s3_bucket_name, Key=filename)
    log_data = s3_object['Body'].read()

    # gzipファイルを解凍
    with gzip.open(log_data, 'rt', encoding='utf-8') as file:
        lines = file.readlines()

    # "TEST"文字列の行をカウント
    test_count = sum(1 for line in lines if "TEST" in line)

    # カウント結果を出力
    print(f"ファイル: {filename}, TESTの行数: {test_count}")

    # ファイルを削除
    os.remove(filename)

def process_files():
    # S3のリストオブジェクトページネーターを作成
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=s3_bucket_name, Prefix=s3_prefix)

    for page in page_iterator:
        for item in page.get('Contents', []):
            file_name = item['Key']
            
            # ファイル名が指定の形式に一致するか確認
            if re.match(file_pattern, os.path.basename(file_name)):
                download_and_process_file(file_name)

if __name__ == "__main__":
    process_files()
