import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    # 이미지 업로드시 content_Type을 지정하지 않으면 버킷에서 url_img클릭하면 이미지 다운로드로 작동해 브라우저에서 이미지 오픈하기위함

    s3_client = boto3.client('s3')
    content_Type = ''
    try:
        if 'jpg' in file_name:
            content_Type = 'image/jpg'
        elif 'jpeg' in file_name:
            content_Type = 'image/jpeg'

        response = s3_client.upload_file(
            file_name,
            bucket,
            object_name,
            ExtraArgs={"ContentType": content_Type}
            )

    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_file(bucket, filname, img_path):
    '''
    img_path : 다운받은 이미지 저장 경로 설정
    '''
    s3 = boto3.client('s3')
    s3.download_file(bucket, filname, img_path)