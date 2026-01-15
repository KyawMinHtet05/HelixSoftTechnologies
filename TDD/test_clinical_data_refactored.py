import pytest
import tempfile
from pathlib import Path
import csv
import re

class ClinicalDataProcessor:
    def __init__(self, ftp_host, ftp_user, ftp_pass, remote_dir=""):
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.connected = False
    
    def connect(self, status_queue=None):
        self.connected = True
        return True
    
    def disconnect(self):
        self.connected = False
    
    def get_file_list(self, status_queue=None):
        return []

class ClinicalDataValidator:
    def __init__(self, download_dir, archive_dir, error_dir):
        self.download_dir = Path(download_dir)
        self.archive_dir = Path(archive_dir)
        self.error_dir = Path(error_dir)
    
    def _validate_filename_pattern(self, filename, status_queue=None):
        pattern = r'^CLINICALDATA\d{14}\.CSV$'
        return bool(re.match(pattern, filename, re.IGNORECASE))
    
    def _validate_csv_content(self, file_path, status_queue=None):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)
                expected = ["PatientID", "TrialCode", "DrugCode", "Dosage_mg", 
                          "StartDate", "EndDate", "Outcome", "SideEffects", "Analyst"]
                return header == expected, [], 1
        except:
            return False, ["Test error"], 0

@pytest.fixture
def temp_dirs():
    with tempfile.TemporaryDirectory() as tmp:
        download = Path(tmp) / "download"
        archive = Path(tmp) / "archive"
        error = Path(tmp) / "error"
        yield download, archive, error

@pytest.fixture
def processor():
    return ClinicalDataProcessor("localhost", "test", "pass")

@pytest.fixture
def validator(temp_dirs):
    return ClinicalDataValidator(*temp_dirs)

class TestProcessor:
    def test_creation(self, processor):
        assert processor.ftp_host == "localhost"
        assert processor.ftp_user == "test"
    
    def test_connection(self, processor):
        assert processor.connect() is True
        assert processor.connected is True
    
    def test_disconnect(self, processor):
        processor.connect()
        processor.disconnect()
        assert processor.connected is False

class TestValidator:
    def test_filename_valid(self, validator):
        valid = "CLINICALDATA20240101120000.CSV"
        assert validator._validate_filename_pattern(valid) is True
    
    def test_filename_invalid(self, validator):
        invalid = "WRONGFILE.CSV"
        assert validator._validate_filename_pattern(invalid) is False