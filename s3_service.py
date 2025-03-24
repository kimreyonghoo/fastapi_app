import boto3
import os
from internal.aws_config import s3_client, S3_BUCKET_NAME  # ✅ aws_config에서 S3_BUCKET_NAME 가져오기
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

# .env 파일 로드
load_dotenv()

# S3 설정
AWS_ACCESS_KEY_ID = os.getenv("AKIA4MI2JTV235FBXI4D")
AWS_SECRET_ACCESS_KEY = os.getenv("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")
AWS_REGION = os.getenv("ap-southeast-2")
AWS_S3_BUCKET_NAME = os.getenv("fastapi-app-koreatech-bucket")


# S3 클라이언트 생성
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# ✅ S3 업로드 함수
def upload_file_to_s3(file_path: str, file_name: str):
    try:
        if not file_path or not file_name:
            raise ValueError("🚨 업로드할 파일 경로나 파일명이 없습니다!")

        print(f"📂 업로드할 파일 경로: {file_path}")
        print(f"📄 업로드할 파일 이름: {file_name}")
        print(f"📦 S3 버킷 이름: {S3_BUCKET_NAME}")  # ✅ 버킷 이름 디버깅 추가

        # ✅ 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"🚨 파일을 찾을 수 없습니다: {file_path}")

        s3_key = f"uploads/{file_name}"
        print(f"📦 S3 업로드 키: {s3_key}")

        # ✅ boto3 업로드 실행 및 예외 처리
        try:
            s3_client.upload_file(file_path, S3_BUCKET_NAME, s3_key)
            print("✅ S3 업로드 성공!")
            return {"message": "Upload Successful", "url": f"https://{S3_BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_key}"}
        except Exception as e:
            raise RuntimeError(f"🚨 S3 업로드 중 오류 발생: {str(e)}")

    except Exception as e:
        raise RuntimeError(f"🚨 최종 오류: {str(e)}")

# ✅ S3 파일 삭제 함수
def delete_file_from_s3(file_name: str):
    try:
        if not file_name:
            raise ValueError("🚨 삭제할 파일명이 없습니다!")

        s3_key = f"uploads/{file_name}"
        print(f"🗑️ S3 삭제 요청: {s3_key}")

        # ✅ 파일 삭제 요청
        response = s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=s3_key)

        # ✅ 응답 확인
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 204:
            print(f"✅ S3에서 삭제 완료: {file_name}")
            return {"message": "Delete Successful", "file": file_name}
        else:
            raise RuntimeError(f"🚨 S3 삭제 실패: {response}")

    except Exception as e:
        raise RuntimeError(f"🚨 S3 삭제 중 오류 발생: {str(e)}")