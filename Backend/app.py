from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import Response
from reasoning import main
from models import *
from pypdf import PdfReader
import io
from pydantic import ValidationError
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the ModuleMatch API!"}


# Add GET /test endpoint for browser access
@app.get("/test")
def test():
    data = main("reasoning")
    print(data)
    return {"data": data}


@app.post("/submit-profile/")
async def submit_profile(
    # 1. Tell FastAPI to accept 'profile' as a raw string
    profile: str = Form(...), 
    cv_pdf: UploadFile = File(...)
):
    # 2. Parse the incoming JSON string into your Pydantic model
    try:
        profile_data = UserProfile.model_validate_json(profile)
    except ValidationError:
        raise HTTPException(status_code=422, detail="Invalid JSON format in profile data.")

    # 3. Safety check for the PDF
    if cv_pdf.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    # 4. Read and extract PDF text
    file_bytes = await cv_pdf.read()
    pdf_file_obj = io.BytesIO(file_bytes)
    
    try:
        reader = PdfReader(pdf_file_obj)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += (page.extract_text() or "") + "\n"
    except Exception:
        raise HTTPException(status_code=422, detail="Could not parse the PDF document.")
    
    # 5. Return the data (Notice we use profile_data here, not profile)
    data = {
        "status": "Success",
        "student_name": profile_data.name,
        "year": profile_data.year,
        "course": profile_data.course,
        "interests": profile_data.interests,
        "goals": profile_data.goals,
        "cv_text": extracted_text
    }
    response = main(data)
    return {"data": response}
