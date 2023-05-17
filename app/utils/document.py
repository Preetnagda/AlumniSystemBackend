import uuid
import boto3
import os
from app.models import User
from app import db
from app.utils.config import Config

BUCKET = Config().S3_BUCKET_NAME

def get_certificate_number():
    return str(uuid.uuid4())

def upload_and_remove_document(file_name):
    s3 = boto3.resource('s3')
    s3.Bucket(BUCKET).upload_file(f"{file_name}.txt", f"{file_name}.txt")
    os.remove(f"{file_name}.txt")
    return True
    
def create_transcript(user: User):
    file_name = get_certificate_number()
    with open(f'{file_name}.txt', 'w') as f:
        f.write('University Transcript\n')
        f.write(f'This is a transcript for {user.first_name} {user.last_name}\n')
        f.write('IT Infrastructure & Security\n')
        f.write('Score: 75/100\n')
    return file_name

def create_certificate(user: User):
    file_name = get_certificate_number()
    with open(f'{file_name}.txt', 'w') as f:
        f.write('University Certificate\n')
        f.write(f'This is to certify that {user.first_name} {user.last_name}\n')
        f.write('has successfully graduated from the university.')
    return file_name

def add_documents_for_user(user: User):
    auto_upload = os.environ.get("AUTO_UPLOAD_FILE", None)
    if not auto_upload:
        return False
    
    certificate_id = create_certificate(user)
    transcript_id = create_transcript(user)

    upload_and_remove_document(certificate_id)
    upload_and_remove_document(transcript_id)

    db.add_document(certificate_id, user, "certificate")
    db.add_document(transcript_id, user, "transcript")