# AWS-S3-utils
____



### Git Clone

```
git clone https://github.com/variety82/AWS-S3-utils.git
```

### Prerequisite

```
$ pip install -r requirements.txt
```



### 주의사항

사용자의 PC - 사용자명 - .aws내에 credentials파일을 넣어줘야 boto3의 client, resource에서 인식합니다.

해당폴더에 credentials파일이 없다면 boto3.cliente, boto3.resource내에 일일이 aws_access_key_id, aws_secret_access_key를 지정해주어야 합니다.

```
# 아래는 예시입니다.
client = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                      )
```

### Files

- `getS3contents.py` : S3에 있는 이미지의 정보를 반환하는 함수(날짜, 시간, 이미지 url 등)
- `S3_file_management.py` : S3 Bucket에 이미지를 업로드, 다운로드하는 함수



#### 사용예시

```
make_objects_list('smartfarmtv')
=> ['빨간달팽이', '파란달팽이']

make_object('smartfarmtv', '빨간달팽이')
=>s3.Object(bucket_name='smartfarmtv', key='빨간달팽이.png')

get_image_type(object)
=> png

get_image_date(object)
=> ('2022-06-19', '15:51')

get_image_url(object)
=> https://~~~~~
```

