import os
from dotenv import load_dotenv
from fastapi import FastAPI

from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
import magic
import uvicorn
from fastapi import FastAPI, HTTPException, Response, UploadFile, status
from loguru import logger



load_dotenv()


app = FastAPI()

# session = boto3.Session(
#     aws_access_key_id='aws_access_key_id',
#     aws_secret_access_key='aws_secret_access_key',
# )

# s3_client = boto3.client('s3', region_name='ap-south-1')


KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

AWS_BUCKET = 'dsc-api-bucket'

s3 = boto3.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)

async def s3_upload(contents: bytes, key: str):
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)



# @app.get("/checkid")
# def read_root():
#     secret_key = os.environ.get("aws_access_key_id")
#     return {"Hello": "World", "ID": secret_key}

# @app.get("/checkkey")
# def read_root():
#     secret_key = os.environ.get("aws_secret_access_key")
#     return {"Hello": "World", "SC": secret_key}


@app.post('/upload')
async def upload(file: UploadFile):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!!'
        )

    contents = await file.read()
    size = len(contents)

    if not 0 < size <= 1 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 1 MB'
        )

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
        )
    file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
    await s3_upload(contents=contents, key=file_name)
    return {'file_name': file_name}




if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)














# import os
# from dotenv import load_dotenv, dotenv_values
# from uuid import uuid4
# import boto3
# from botocore.exceptions import ClientError
# import magic
# import uvicorn
# from fastapi import FastAPI, HTTPException, Response, UploadFile, status
# from loguru import logger
# import io
# from decouple import config
# from decouple import Config, Csv

# # Create a Config object
# # access_key_int = int('ACCESS_KEY')
# # config = Config(access_key_int)


# load_dotenv()



# # Read AWS credentials and S3 bucket name from .env file
# aws_access_key_id = config('ACCESS_KEY')
# aws_secret_access_key = config('SECRET_KEY')
# s3_bucket_name = config('AWS_BUCKET_NAME')

# # # AWS_BUCKET_NAME='dsc-api-bucket',
# # AWS_DOMAIN = "AWS_DOMAIN"

# print(os.getenv("aws_secret_access_key"))

# # Create an S3 client
# s3 = boto3.client(
#     's3',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key
# )


# app = FastAPI()

# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}

# @app.post("/upload/")
# async def upload_file(file_data: bytes):
#     # Define the S3 object key (file name)
#     object_key = "example.jpg"  # You can replace this with your desired object key

#     # Upload the file to the S3 bucket
#     s3.upload_fileobj(
#         Fileobj=io.BytesIO(file_data),
#         Bucket=s3_bucket_name,
#         Key=object_key
#     )

#     return {"message": "File uploaded successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# KB = 1024
# MB = 1024 * KB

# SUPPORTED_FILE_TYPES = {
#     'image/png': 'png',
#     'image/jpeg': 'jpg',
#     'application/pdf': 'pdf'
# }

# AWS_BUCKET = 'AWS_BUCKET_NAME'

# s3 = boto3.resource('s3')
# bucket = s3.Bucket('AWS_BUCKET')


# async def s3_upload(contents: bytes, key: str):
#     logger.info(f'Uploading {key} to s3')
#     bucket.put_object(Key=key, Body=contents)


# # async def s3_download(key: str):
# #     try:
# #         return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
# #     except ClientError as err:
# #         logger.error(str(err))

# app = FastAPI()


# @app.get('/')
# async def home():
#     return {'message': 'Hello from file-upload 😄👋'}


# @app.post('/upload')
# async def upload(file: UploadFile ):
#     if not file:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='No file found!!'
#         )

#     contents = await file.read()
#     size = len(contents)

#     if not 0 < size <= 1 * MB:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Supported file size is 0 - 1 MB'
#         )

#     file_type = magic.from_buffer(buffer=contents, mime=True)
#     if file_type not in SUPPORTED_FILE_TYPES:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
#         )
#     file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'

#     try:
#         s3.Object(AWS_BUCKET, file_name).put(Body=io.BytesIO(contents))
#     except ClientError as e:
#         logger.error(f"Failed to upload file to S3: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail='Failed to upload file to S3'
#         )
#     await s3_upload(contents=contents, key=file_name)
#     return {'file_name': file_name}


# # @app.get('/download')
# # async def download(file_name: str | None = None):
# #     if not file_name:
# #         raise HTTPException(
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #             detail='No file name provided'
# #         )

# #     contents = await s3_download(key=file_name)
# #     return Response(
# #         content=contents,
# #         headers={
# #             'Content-Disposition': f'attachment;filename={file_name}',
# #             'Content-Type': 'application/octet-stream',
# #         }
# #     )

# if __name__ == '__main__':
#     uvicorn.run(app='main:app', reload=True)


