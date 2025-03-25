from fastapi import APIRouter, File, UploadFile, HTTPException
import boto3
import os
from dotenv import load_dotenv
from internal.aws_config import aws_access

load_dotenv()  # 환경 변수 로드

router = APIRouter()

# AWS S3 설정

S3_BUCKET_NAME = "fastapi-app-koreatech-bucket"
S3_REGION = "ap-southeast-2"  # 서울 리전 예시

# S3 클라이언트 생성
s3_client = boto3.client(
    "s3",
    region_name=aws_access['region_ap'],
    aws_access_key_id=aws_access['aws_access_key_id'],
    aws_secret_access_key=aws_access['aws_secret_access_key']
)

@router.post("/upload")
async def upload_to_s3(file: UploadFile = File(...)):
    """Flutter에서 받은 사진을 S3에 업로드"""
    try:
        file_path = f"uploads/{file.filename}"  # S3 내부 저장 경로
        s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file_path, ExtraArgs={"ACL": "public-read"})

        s3_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{file_path}"
        return {"message": "File uploaded successfully", "url": s3_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
