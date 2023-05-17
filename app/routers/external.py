from fastapi.responses import FileResponse, StreamingResponse
from fastapi import HTTPException, APIRouter, Response, BackgroundTasks
from app.utils.config import Config
from app import db
import boto3
import os

router = APIRouter(tags=["Open"])

@router.get("/download_document")
def download_document(document_no: str, background_tasks: BackgroundTasks):
    s3 = boto3.client("s3")
    try:
        document_details = db.get_document(document_no)
        output_file_name = document_details.type + ".txt"
        s3.download_file(Bucket=Config().S3_BUCKET_NAME, Key=document_no+".txt", Filename=f"app/tmp/{document_no}.txt")
        background_tasks.add_task(os.remove, f"./app/tmp/{document_no}.txt")
        return FileResponse(f"app/tmp/{document_no}.txt", media_type='application/octet-stream', filename=output_file_name)
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise Exception(e)