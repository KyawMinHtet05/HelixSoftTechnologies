import pytest
import tempfile
import os
from pathlib import Path
import csv
import uuid
from datetime import datetime
import re

class ClinicalDataProcessor:
    def __init__(self, ftp_host, ftp_user, ftp_pass, remote_dir=""):
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.remote_dir = remote_dir
        self.ftp = None
        self.connected = False

class ClinicalDataValidator:
    def __init__(self, download_dir, archive_dir, error_dir):
        self.download_dir = Path(download_dir)
        self.archive_dir = Path(archive_dir)
        self.error_dir = Path(error_dir)
        
        for directory in [self.download_dir, self.archive_dir, self.error_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _validate_filename_pattern(self, filename, status_queue=None):
        pattern = r'^CLINICALDATA\d{14}\.CSV$'
        return re.match(pattern, filename, re.IGNORECASE) is not None
    
    def _validate_csv_content(self, file_path, status_queue=None):
        errors = []
        valid_records = []
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                
                try:
                    header = next(reader)
                    expected_fields = ["PatientID", "TrialCode", "DrugCode", "Dosage_mg", 
                                     "StartDate", "EndDate", "Outcome", "SideEffects", "Analyst"]
                    if header != expected_fields:
                        errors.append(f"Invalid header")
                        return False, errors, 0
                except StopIteration:
                    errors.append("File is empty")
                    return False, errors, 0
                
                row_num = 1
                for row in reader:
                    row_num += 1
                    record_errors = []
                    
                    if len(row) != 9:
                        errors.append(f"Row {row_num}: Expected 9 fields, got {len(row)}")
                        continue
                    
                    valid_records.append(row)
            
            if errors:
                return False, errors, len(valid_records)
            return True, [], len(valid_records)
            
        except UnicodeDecodeError:
            return False, ["File is not valid UTF-8 encoded CSV"], 0
        except Exception as e:
            return False, [f"File read error: {str(e)}"], 0

    def test_processor_creation(self):
        processor = ClinicalDataProcessor("localhost", "test", "password")
        assert processor.ftp_host == "localhost"
        assert processor.ftp_user == "test"
        assert processor.ftp_pass == "password"
        assert not processor.connected

class TestClinicalDataValidator:
    @pytest.fixture
    def temp_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            download = Path(tmpdir) / "download"
            archive = Path(tmpdir) / "archive"
            error = Path(tmpdir) / "error"
            yield download, archive, error
    
    def test_validator_creation(self, temp_dirs):
        download, archive, error = temp_dirs
        validator = ClinicalDataValidator(download, archive, error)
        assert validator.download_dir.exists()
        assert validator.archive_dir.exists()
        assert validator.error_dir.exists()
    
    def test_filename_validation_valid(self):
        download, archive, error = temp_dirs = (Path(), Path(), Path())
        validator = ClinicalDataValidator(*temp_dirs)
        
        valid_names = [
            "CLINICALDATA20240101120000.CSV",
            "CLINICALDATA20241231235959.CSV",
            "clinicaldata20240101120000.csv"  
        ]
        
        for filename in valid_names:
            assert validator._validate_filename_pattern(filename) is True
    
    def test_filename_validation_invalid(self):
        download, archive, error = temp_dirs = (Path(), Path(), Path())
        validator = ClinicalDataValidator(*temp_dirs)
        
        invalid_names = [
            "clinicaldata.csv",
            "CLINICALDATA.CSV",
            "CLINICALDATA20240101.CSV",  
            "DATA20240101120000.CSV",  
            "CLINICALDATA20240101120000.TXT"  
        ]
        
        for filename in invalid_names:
            assert validator._validate_filename_pattern(filename) is False