from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import litellm
import pypdf
import io
from .crew import Floagentdemo
from typing import Any

litellm._turn_on_debug()

def serialize_crew_output(obj: Any) -> Any:
    """Helper function to serialize CrewAI output"""
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    elif isinstance(obj, (list, tuple)):
        return [serialize_crew_output(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_crew_output(value) for key, value in obj.items()}
    else:
        return str(obj)

app = FastAPI(title="FloAgent API", description="API for processing PDFs using CrewAI")

@app.post("/process-pdf")
async def process_pdf(file: UploadFile):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Read the uploaded file
        content = await file.read()
        pdf_file = io.BytesIO(content)
        
        # Parse PDF
        pdf_reader = pypdf.PdfReader(pdf_file)
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Process with CrewAI
        inputs = {
            'statement_text': text_content,
        }
        
        try:
            result = Floagentdemo().crew().kickoff(inputs=inputs)
            # Serialize the CrewAI output
            serialized_result = serialize_crew_output(result)
            return JSONResponse(content={
                "message": "PDF processed successfully",
                "result": "success"
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in CrewAI processing: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to FloAgent API. Use /process-pdf endpoint to process PDF documents."} 
