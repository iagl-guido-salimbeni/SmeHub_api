# SmeHub Report API

A FastAPI backend service for processing business report requests with Firebase Firestore integration.

## Features

- FastAPI web framework with automatic API documentation
- Firebase Firestore integration for data persistence
- Dummy report generation (placeholder for AI-powered reports)
- CORS support for frontend integration
- Comprehensive error handling and logging
- Health check endpoint

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Firebase

You have two options for Firebase configuration:

#### Option A: Service Account Key File (Recommended for Development)

1. Download your Firebase service account key JSON file from the Firebase Console
2. Place it in your project directory
3. Create a `.env` file and add:
```
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/serviceAccountKey.json
```

#### Option B: Environment Variables (Recommended for Production)

1. Copy `.env.example` to `.env`
2. Fill in your Firebase configuration values:
```bash
cp .env.example .env
```

Then edit `.env` with your Firebase project details:
```
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account-email@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
```

### 3. Run the Application

#### Development Mode
```bash
python main.py
```

#### Production Mode with Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### With Auto-reload (Development)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check
- **GET** `/` - Basic health check
- **GET** `/health` - Detailed health check with Firebase connection status

### Report Processing
- **POST** `/api/request-report` - Process a report request

#### Request Body Example:
```json
{
  "reportId": "firestore-document-id",
  "userId": "user-id",
  "businessInfo": {
    "businessName": "Acme Corp",
    "postalCode": "90210",
    "country": "United States",
    "industry": "Technology"
  },
  "finalPrompt": "Generate a market analysis report focusing on competitive landscape and growth opportunities."
}
```

#### Response Example:
```json
{
  "success": true,
  "message": "Report generated successfully",
  "reportId": "firestore-document-id"
}
```

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
├── main.py              # Main FastAPI application
├── firebase_config.py   # Firebase configuration and initialization
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .env                # Your environment variables (create this)
└── README.md           # This file
```

## Firebase Firestore Integration

The API integrates with Firebase Firestore to:

1. **Update Report Status**: Changes status from `pending_backend_processing` to `processing` to `completed` or `failed`
2. **Store Generated Reports**: Saves the generated report content to the `generatedReport` field
3. **Track Timestamps**: Updates `updatedAt` and `completedAt` timestamps

### Expected Firestore Document Structure

```javascript
{
  userId: "user-id",
  businessInfo: {
    businessName: "Company Name",
    postalCode: "12345",
    country: "Country",
    industry: "Industry"
  },
  finalPrompt: "Report generation prompt",
  status: "completed", // pending_backend_processing | processing | completed | failed
  generatedReport: "Generated report content in markdown format",
  createdAt: Timestamp,
  updatedAt: Timestamp,
  completedAt: Timestamp
}
```

## Development Notes

### Dummy Report Generation

The current implementation includes a `dummy_report_processor` function that:
- Performs a simple calculation (2 + 2 = 4)
- Generates a mock business report in Markdown format
- Uses the provided business information and prompt

**To implement real AI report generation:**
1. Replace the `dummy_report_processor` function with your AI service integration
2. Add any additional dependencies to `requirements.txt`
3. Configure API keys or credentials for your AI service

### Error Handling

The API includes comprehensive error handling:
- Input validation using Pydantic models
- Firebase connection error handling
- Graceful degradation when Firebase is unavailable
- Detailed logging for debugging

### CORS Configuration

The current CORS configuration allows all origins (`*`). For production, update the `allow_origins` list in `main.py` to include only your frontend domains:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Deployment

### Local Development
The application runs on `http://localhost:8000` by default.

### Production Deployment
Consider using:
- **Google Cloud Run** (recommended for Firebase integration)
- **Heroku**
- **AWS Lambda** with Mangum
- **Docker** containers

### Environment Variables for Production
Ensure all sensitive configuration is stored in environment variables, not in code.

## Troubleshooting

### Firebase Connection Issues
1. Verify your service account key file path or environment variables
2. Check that your Firebase project ID is correct
3. Ensure your service account has Firestore read/write permissions

### CORS Issues
If your frontend can't connect to the API, check the CORS configuration in `main.py`.

### Port Conflicts
If port 8000 is in use, specify a different port:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080
