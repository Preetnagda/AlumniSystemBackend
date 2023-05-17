from fastapi.responses import FileResponse, StreamingResponse
from fastapi import HTTPException, APIRouter, Response
from app.utils.config import Config
import boto3

router = APIRouter(tags=["Open"])

@router.get("/download_document")
def download_document(document_no: str):
    s3 = boto3.client("s3")
    try:
        result = s3.get_object(Bucket=Config().S3_BUCKET_NAME, Key=document_no+".txt")
        # FileResponse(file_location, media_type='application/octet-stream',filename=file_name)
        return StreamingResponse(content=result["Body"].iter_chunks())
        # return Response(result)
    except Exception as e:
        if hasattr(e, "message"):
            raise HTTPException(
                status_code=e.message["response"]["Error"]["Code"],
                detail=e.message["response"]["Error"]["Message"],
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))
