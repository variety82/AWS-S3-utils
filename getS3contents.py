import boto3
import datetime

def get_all_objects(s3, **base_kwargs):
    continuation_token = None
    while True:
        list_kwargs = dict(MaxKeys=1000, **base_kwargs)
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token
        response = s3.list_objects_v2(**list_kwargs)
        yield from response.get('Contents', [])
        if not response.get('IsTruncated'):  
            break
        continuation_token = response.get('NextContinuationToken')

def make_objects_list(BucketName):
    """
    bucket에 존재하는 객체명들을 리스트로 생성
    """
    with open("output.txt", "w") as f:
        for file in get_all_objects(boto3.client('s3'), Bucket=BucketName):
            f.write(file['Key']+'\n')

    with open('./output.txt', 'r') as f:
        objects_list = f.readlines()
        for idx, obj in enumerate(objects_list):
            objects_list[idx] = obj.strip()
    return objects_list

def make_object(bucketname, objectname):
    """
    S3의 해당 bucket에서 원하는 객체의 정보를 리턴
    객체정보 : bucket_name, key(file name)
    """
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucketname)
    return bucket.Object(objectname)

def get_image_type(object):
    """
    s3에 올리기위한 이미지 확장자를 리턴
    url, 저장형식을 위함
    """
    return object.get()['ContentType'][6:]

def get_image_date(object):
    """
    해당 이미지의 최근 수정 날짜, 시간을 return
    기준 시간이 한국이 아니기에 한국 시간으로 변경
    이미지 업로드 후 수정한적이 없다면 업로드 날짜로 생성
    """
    KST = datetime.timedelta(hours=9)

    obj = object.get()['LastModified']
    korea_time = str(obj + KST).split()

    date, time = korea_time[0], korea_time[1][:5]
    return date, time

def get_image_url(object):
    """
    S3 bucket에 있는 이미지의 url을 return
    """
    filename = object.key
    bucketname = object.bucket_name
    s3_client = boto3.client('s3')
    location = s3_client.get_bucket_location(Bucket=bucketname)["LocationConstraint"]

    return f"https://{bucketname}.s3.{location}.amazonaws.com/{filename}"