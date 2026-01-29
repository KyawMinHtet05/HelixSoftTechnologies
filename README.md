📋 HelixSoft Clinical Data Processor
📖 Overview
The HelixSoft Clinical Data Processor is a robust desktop application designed to securely connect to FTP servers, download clinical trial data files, validate them against strict business rules, and automatically process them into organized archive structures. Built with Python and Tkinter, this tool ensures data integrity and compliance for clinical research organizations.

✨ Key Features
🔐 Secure FTP Connectivity – Connect to FTP servers with configurable credentials and passive mode

📊 Smart File Validation – Comprehensive validation including filename patterns, CSV structure, and data integrity checks

🏷️ GUID Error Tracking – Each error is logged with a unique GUID generated via external API (uuidtools.com) with local fallback

📁 Automated File Processing – Files are automatically sorted into Archive/Error directories based on validation results

🔍 Advanced Search & Filter – Quickly find files with real-time search functionality

📈 Detailed Processing Logs – Color-coded logs for easy monitoring of operations

🐳 Docker Containerization – Easy deployment with Docker support

🧪 Comprehensive Testing – Unit tests, integration tests, and CI/CD pipeline

🛠️ Technology Stack
Language: Python 3.10

GUI Framework: Tkinter

Networking: ftplib, requests

Data Processing: CSV, datetime, re

Containerization: Docker

Testing: pytest, unittest

CI/CD: GitHub Actions

📋 Prerequisites
Python 3.10 or higher

Docker (optional, for containerized deployment)

FTP server access (for testing/actual use)

Tkinter library (usually included with Python)

🚀 Installation
Option 1: Local Installation
Clone the repository

bash
git clone https://github.com/yourusername/helixsoft-clinical-data-processor.git
cd helixsoft-clinical-data-processor
Create virtual environment

bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python HelixSoftTechnologies.py
Option 2: Docker Installation
Build Docker image

bash
docker build -t helixsoft-clinical-data .
Run Docker container

bash
docker run -it --name helixsoft-app helixsoft-clinical-data
🏗️ Project Structure
text
helixsoft-clinical-data-processor/
│
├── HelixSoftTechnologies.py      # Main application file
├── Dockerfile                    # Docker configuration
├── .github/workflows/            # CI/CD pipelines
│   └── ci-cd.yml
├── requirements.txt              # Python dependencies
├── tests/                        # Test suites
│   ├── test_validator.py
│   ├── test_ftp_processor.py
│   └── test_uuid_integration.py
├── README.md                     # This file
├── .gitignore
└── clinical_data_samples/        # Sample data files (optional)
📁 Directory Structure Created by Application
text
~/ClinicalData/
├── Downloads/                    # Temporary download location
├── Archive/                      # Validated and archived files
│   └── CLINICALDATA_20240101120000_20240115.CSV
├── Errors/                       # Rejected/invalid files
│   ├── CLINICALDATA_20240101120000.CSV
│   └── error_report.log         # Detailed error logs with GUIDs
└── processed_files.txt          # Track processed files
🔧 Configuration
FTP Connection Settings
Host: Your FTP server address (default: localhost)

Username: FTP username (default: kmh)

Password: FTP password (default: 123)

Remote Directory: Optional subdirectory on FTP server

File Validation Rules
Filename Pattern: Must match CLINICALDATA_YYYYMMDDHHMMSS.CSV

CSV Structure: Must have exactly 9 columns with specific headers

Data Validation:

PatientID: Required

TrialCode: Required

DrugCode: Required

Dosage_mg: Positive integer

StartDate/EndDate: Valid dates in YYYY-MM-DD format

Outcome: Must be "Improved", "No Change", or "Worsened"

SideEffects: Text field

Analyst: Required

📊 Usage Guide
1. Connecting to FTP Server
Enter FTP credentials in the left panel

Click "🔌 Connect"

Verify connection status changes to green

2. Viewing Server Files
All server files appear in the middle panel

Use search box to filter files

Click "🔄 Refresh" to update file list

3. Validating Files
Select a CSV file from the list

Click "🔍 Validate Selected File"

View validation results in the log panel

4. Processing Files
Select a CSV file from the list

Click "🚀 Process Selected File"

Confirm processing in the dialog

Monitor progress in the log panel

5. Reviewing Results
Valid files: Archived with date suffix

Invalid files: Moved to Errors folder with error log entry

Error log: Access via "📂 Open Error Log" button

🧪 Testing
Running Tests Locally
bash
# Run all tests
pytest -v

# Run specific test modules
python -m pytest tests/test_validator.py -v
python -m pytest tests/test_ftp_processor.py -v
python -m pytest tests/test_uuid_integration.py -v
Test Categories
Unit Tests: Individual component testing

Integration Tests: Component interaction testing

UUID Integration Tests: External API and fallback testing

🔄 CI/CD Pipeline
The project includes GitHub Actions CI/CD pipeline that:

✅ Runs automated tests on push/pull requests

✅ Builds Docker image on successful tests

✅ Pushes to Docker Hub on main branch updates

Pipeline Triggers
Push to main/master branch

Pull requests to main/master branch

Manual workflow dispatch

🐳 Docker Deployment
Build Arguments
Base image: Python 3.10

Includes X11 display support for GUI

Pre-configured directories

Environment Variables
bash
DISPLAY=host.docker.internal:0  # For GUI display
🚨 Error Handling
GUID Generation Strategy
Primary: External API call to uuidtools.com (5s timeout)

Fallback: Local UUID generation if API fails

Logging: All errors logged with GUID for tracking

Error Categories
Connection Errors: FTP connectivity issues

Validation Errors: File format/content violations

Processing Errors: File system/archival failures

📝 Logging System
Log Levels & Colors
INFO: Blue - General information

SUCCESS: Green - Successful operations

WARNING: Orange - Non-critical issues

ERROR: Red - Critical failures

COMPLETE: Cyan - Process completion

SUMMARY: Purple - Final summaries

Error Log Format
text
[2024-01-15 10:30:45] GUID: 123e4567-e89b-12d3-a456-426614174000 | File: CLINICALDATA_20240101120000.CSV | Error: Invalid header format
🔒 Security Considerations
Password Handling: Passwords stored in memory only during session

FTP Security: Uses passive mode for firewall compatibility

Data Isolation: Each validation run in isolated temporary files

Error Obfuscation: Sensitive details not exposed in error messages

🚀 Performance Optimizations
Background Processing: GUI remains responsive during file operations

File Caching: Processed files tracked to avoid reprocessing

Memory Management: Large files processed in chunks

Connection Pooling: FTP connections managed efficiently

🐛 Troubleshooting
Common Issues
GUI Not Displaying in Docker

bash
# Ensure X11 server is running
xhost +localhost
# Run with proper display
docker run -e DISPLAY=host.docker.internal:0 helixsoft-clinical-data
FTP Connection Failures

Verify network connectivity

Check firewall settings

Confirm credentials

File Processing Errors

Check available disk space

Verify directory permissions

Review error logs

Debug Mode
Add debug logging by modifying the logging configuration in the main application file.

📈 Monitoring & Metrics
Key Metrics Tracked
Files processed per session

Validation success rate

Average processing time

Error frequency by category

Log Analysis
Error logs can be analyzed using standard log analysis tools or custom scripts to identify patterns and recurring issues.

🔮 Future Enhancements
Database Integration: Store processing metadata in SQL database

Web Interface: REST API for remote processing

Advanced Analytics: Data quality dashboards

Batch Processing: Support for multi-file operations

Cloud Integration: AWS S3/Azure Blob storage support

Email Notifications: Alert system for critical errors

Custom Validation Rules: User-defined validation schemas

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

Development Guidelines
Write unit tests for new features

Maintain code coverage > 80%

Follow PEP 8 style guide

Update documentation for changes

📄 License
This project is proprietary software. All rights reserved.

👥 Support
For support, please contact:

Development Team: dev@helixsoft.com

System Administrator: admin@helixsoft.com

Documentation: docs@helixsoft.com

📊 Sample Data Format
csv
PatientID,TrialCode,DrugCode,Dosage_mg,StartDate,EndDate,Outcome,SideEffects,Analyst
PAT001,TRIAL-2024-A,DRUG-XYZ,50,2024-01-01,2024-03-01,Improved,None,Dr. Smith
PAT002,TRIAL-2024-A,DRUG-XYZ,50,2024-01-02,2024-03-02,No Change,Headache,Dr. Smith
