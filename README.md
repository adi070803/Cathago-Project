# Credit-Based Document Scanning System

## Overview:
This is a **self-contained** web application for **document scanning and matching** with a **credit-based system**. Users have a daily limit of **20 free scans**, and additional scans require **admin-approved credits**. 

## Features
- **User Authentication** (Signup, Login, Roles: User & Admin)
- **Credit System** (20 free scans per day, admin approval for more credits)
- **Document Upload & Matching** (Basic text matching & AI-powered analysis)
- **Admin Analytics Dashboard** (Tracks scan activity, top users, and credit usage)
- **Dark Mode UI with Smooth Animations**

## Tech Stack:
- **Frontend:** HTML, CSS (Custom Animations), JavaScript
- **Backend:** Flask (Python), SQLite (Local Storage)
- **Authentication:** Username-Password (Hashed)
- **File Storage:** Local File System (`static/uploads/`)
- **Text Matching:** Basic Algorithm (Levenshtein Distance), AI-based Matching (Optional)

## Installation:

### **1. Clone the repository**
```bash
git clone https://github.com/adi070803/Cathago-Project.git
cd Cathago-Project
```

### **2. Set up Backend:**
#### Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

#### Run the Flask server:
```bash
python app.py
```
The backend runs on **http://127.0.0.1:5000**

### **3. Set up Frontend:**
Simply open `frontend/index.html` in a browser.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | User login |
| GET | `/user/profile` | Get user credits & details |
| POST | `/scan/upload` | Upload document for scanning (uses 1 credit) |
| POST | `/credits/request` | Request admin to add credits |
| GET | `/admin/analytics` | Get analytics for admins |


## Notes:
- **Daily credit resets at midnight** (local server time)
- **Admin can approve/deny credit requests manually**
- **AI-based matching** – Requires OpenAI API Key

