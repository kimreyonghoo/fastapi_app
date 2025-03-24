from fastapi import APIRouter, UploadFile, File, HTTPException
from s3_service import upload_file_to_s3, delete_file_from_s3
import os

router = APIRouter()

UPLOAD_DIR = "temp"

# ✅ temp 폴더 자동 생성
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        if file is None or not file.filename:
            raise HTTPException(status_code=400, detail="🚨 파일이 없습니다.")

        file_location = os.path.join(UPLOAD_DIR, file.filename)

        # ✅ 파일 저장 (비동기 방식)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        print(f"📂 파일 저장 완료: {file_location}")

        # ✅ S3 업로드 (파일 경로와 파일명 전달)
        s3_response = upload_file_to_s3(file_location, file.filename)

        # ✅ 로컬 파일 삭제
        os.remove(file_location)

        return s3_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 업로드 실패: {str(e)}")

# ✅ S3 파일 삭제 엔드포인트
@router.delete("/delete/")
async def delete_file(file_name: str):
    try:
        if not file_name:
            raise HTTPException(status_code=400, detail="🚨 파일명이 필요합니다.")

        result = delete_file_from_s3(file_name)  # ✅ 삭제 함수 호출
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 파일 삭제 실패: {str(e)}")
