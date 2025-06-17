from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv
from firebase_admin import firestore
from datetime import datetime
import logging
from firebase_config import initialize_firebase

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SmeHub Report API",
    description="API for processing business report requests",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase
db = initialize_firebase()
if db:
    logger.info("Firebase initialized successfully")
else:
    logger.warning("Firebase not initialized - running in demo mode")

# Pydantic models for request/response
class BusinessInfo(BaseModel):
    businessName: str
    postalCode: str
    country: str
    industry: str

class ReportRequest(BaseModel):
    reportId: str
    userId: str
    businessInfo: BusinessInfo
    finalPrompt: str

class ReportResponse(BaseModel):
    success: bool
    message: str
    reportId: str

# Dummy processing function
def dummy_report_processor(business_info: BusinessInfo, prompt: str) -> str:
    """
    Dummy function that performs a simple calculation and generates a mock report.
    Replace this with your actual AI report generation logic.
    """
    # Simple dummy calculation: 2 + 2 = 4
    calculation_result = 2 + 2
    
    # Generate a dummy report
    dummy_report = f"""
# Business Report for {business_info.businessName}

## Executive Summary
This is a dummy report generated for demonstration purposes.

## Business Information
- **Company**: {business_info.businessName}
- **Location**: {business_info.postalCode}, {business_info.country}
- **Industry**: {business_info.industry}

## Analysis
Based on your request: "{prompt[:100]}..."

Our dummy processing function calculated: 2 + 2 = {calculation_result}

## Key Findings
1. Your business is located in {business_info.country}
2. You operate in the {business_info.industry} industry
3. Our advanced calculation shows that 2 + 2 equals {calculation_result}

## Recommendations
1. Continue operating your business
2. Consider the fact that 2 + 2 = {calculation_result}
3. This is a placeholder report - replace with actual AI-generated content

## Conclusion
This dummy report has been successfully generated. The calculation 2 + 2 = {calculation_result} has been verified.

---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return dummy_report.strip()

async def update_firestore_report(report_id: str, generated_report: str, status: str = "completed"):
    """
    Update the Firestore document with the generated report.
    """
    if db is None:
        logger.warning("Firestore not initialized - skipping database update")
        return False
    
    try:
        doc_ref = db.collection('reports').document(report_id)
        doc_ref.update({
            'generatedReport': generated_report,
            'status': status,
            'updatedAt': firestore.SERVER_TIMESTAMP,
            'completedAt': firestore.SERVER_TIMESTAMP
        })
        logger.info(f"Successfully updated report {report_id} in Firestore")
        return True
    except Exception as e:
        logger.error(f"Failed to update Firestore: {e}")
        return False

# API Routes
@app.get("/")
async def root():
    return {"message": "SmeHub Report API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "firebase_connected": db is not None
    }

@app.post("/api/request-report", response_model=ReportResponse)
async def process_report_request(request: ReportRequest):
    """
    Process a report request from the frontend.
    """
    try:
        logger.info(f"Received report request for reportId: {request.reportId}")
        
        # Validate the request
        if not request.reportId or not request.userId:
            raise HTTPException(status_code=400, detail="Missing required fields: reportId or userId")
        
        # Update status to processing
        if db:
            try:
                doc_ref = db.collection('reports').document(request.reportId)
                doc_ref.update({
                    'status': 'processing',
                    'updatedAt': firestore.SERVER_TIMESTAMP
                })
            except Exception as e:
                logger.warning(f"Could not update status to processing: {e}")
        
        # Process the report using our dummy function
        logger.info("Starting report generation...")
        generated_report = dummy_report_processor(request.businessInfo, request.finalPrompt)
        logger.info("Report generation completed")
        
        # Update Firestore with the generated report
        firestore_updated = await update_firestore_report(request.reportId, generated_report)
        
        if not firestore_updated:
            logger.warning("Firestore update failed, but report was generated")
        
        return ReportResponse(
            success=True,
            message="Report generated successfully",
            reportId=request.reportId
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing report request: {e}")
        
        # Update status to failed if possible
        if db:
            try:
                doc_ref = db.collection('reports').document(request.reportId)
                doc_ref.update({
                    'status': 'failed',
                    'error': str(e),
                    'updatedAt': firestore.SERVER_TIMESTAMP
                })
            except Exception as update_error:
                logger.error(f"Could not update status to failed: {update_error}")
        
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
