import os
import firebase_admin
from firebase_admin import credentials, firestore
import json
from typing import Optional

def initialize_firebase() -> Optional[firestore.Client]:
    """
    Initialize Firebase Admin SDK with different configuration options.
    Returns Firestore client if successful, None otherwise.
    """
    try:
        # Check if Firebase is already initialized
        if firebase_admin._apps:
            return firestore.client()
        
        # Option 1: Using service account key file
        service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if service_account_path and os.path.exists(service_account_path):
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        
        # Option 2: Using environment variables to construct service account
        project_id = os.getenv('FIREBASE_PROJECT_ID')
        private_key_id = os.getenv('FIREBASE_PRIVATE_KEY_ID')
        private_key = os.getenv('FIREBASE_PRIVATE_KEY')
        client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
        client_id = os.getenv('FIREBASE_CLIENT_ID')
        
        if all([project_id, private_key_id, private_key, client_email, client_id]):
            # Replace escaped newlines in private key
            private_key = private_key.replace('\\n', '\n')
            
            service_account_info = {
                "type": "service_account",
                "project_id": project_id,
                "private_key_id": private_key_id,
                "private_key": private_key,
                "client_email": client_email,
                "client_id": client_id,
                "auth_uri": os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                "token_uri": os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email}"
            }
            
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            return firestore.client()
        
        # Option 3: Default credentials (for Google Cloud environments)
        try:
            firebase_admin.initialize_app()
            return firestore.client()
        except Exception:
            pass
        
        print("Warning: No Firebase credentials found. Please configure your Firebase settings.")
        return None
        
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def get_firestore_client() -> Optional[firestore.Client]:
    """
    Get Firestore client, initializing Firebase if needed.
    """
    try:
        return firestore.client()
    except ValueError:
        # Firebase not initialized yet
        return initialize_firebase()
