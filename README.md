# 🧬 HelixSoft Clinical Data Processor

A **desktop-based clinical CSV data processing system** built with **Python (Tkinter)** that connects to an **FTP server**, validates clinical trial data files, and safely archives or rejects them based on strict business and data integrity rules.

The system is fully **Dockerized**, supports **CI/CD using GitHub Actions**, and follows **TDD and unit testing best practices**.

---

## 📌 Key Features

### 🔌 FTP Integration
- Secure FTP connection with passive mode
- Remote directory support
- Live file listing and refresh
- Safe connect / disconnect handling

### 📂 File Management
- Download clinical CSV files from FTP
- Archive valid files with date suffix
- Move invalid files to error directory
- Prevent re-processing of already processed files

### ✅ Data Validation Rules
**Filename Validation**
- Must follow pattern:  
  `CLINICALDATA_YYYYMMDDHHMMSS.CSV`

**CSV Structure Validation**
- Exact header match:


**Record-Level Validation**
- Required fields must not be empty
- Dosage must be a positive integer
- Date format must be `YYYY-MM-DD`
- EndDate must be after StartDate
- Outcome must be one of:
- Improved
- No Change
- Worsened
- Duplicate detection using composite key:



### 🧾 Error Handling & Logging
- Centralized error log (`error_report.log`)
- Each error tagged with:
- Timestamp
- File name
- GUID
- GUID generated using:
- External UUID API (`uuidtools.com`)
- Automatic local fallback (`uuid.uuid4()`)

### 🖥️ Graphical User Interface (GUI)
- Built with **Tkinter**
- Real-time processing logs
- Searchable file list
- Validation and processing buttons
- Color-coded log messages (info, success, warning, error)

---

## 🧪 Testing Strategy

This project follows **Test-Driven Development (TDD)** and includes:

- ✅ Unit tests
- ✅ UUID API integration tests
- ✅ Validation logic tests
- ✅ FTP-independent testing using mocks

Tests are executed automatically in the CI pipeline using **pytest**.

Run tests locally:
```bash
pytest -v

```
## 🐳 Docker Support
Dockerfile Highlights

Python 3.10 base image

Tkinter + X11 support

Xvfb virtual display for GUI compatibility

Required directories auto-created

Build Image Locally

```bash
docker build -t helixsoft-clinical-data .
```

## Run Container
```bash
docker run -it \
  -e DISPLAY=host.docker.internal:0 \
  helixsoft-clinical-data

```

## CI/CD Pipeline (GitHub Actions)
Pipeline Stages

Test Stage

Install dependencies

Run unit tests using pytest

Build & Push Stage

Build Docker image

Push to Docker Hub

Triggered only on push to main

CI/CD File

.github/workflows/ci-cd.yml

```bash
.
├── HelixSoftTechnologies.py
├── Dockerfile
├── requirements.txt
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── tests/
│   ├── test_validation.py
│   ├── test_uuid_integration.py
│   └── test_processing.py
├── ClinicalData/
│   ├── Downloads/
│   ├── Archive/
│   └── Errors/
└── README.md

```

## ⚙️ Configuration
Default FTP Credentials (Change in GUI)

```bash
Host: localhost
Username: kmh
Password: 123

```
## Local Storage Paths

```bash
~/ClinicalData/Downloads
~/ClinicalData/Archive
~/ClinicalData/Errors


```
