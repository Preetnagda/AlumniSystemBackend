from datetime import datetime

def get_certificate_number(student_id):
    now = datetime.now()
    current_year = now.strftime("%Y")
    return current_year + student_id[1:]