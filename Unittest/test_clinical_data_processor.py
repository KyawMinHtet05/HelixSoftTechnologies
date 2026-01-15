import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
import tempfile
import os
from pathlib import Path

from HelixSoftTechnologies import ClinicalDataValidator, ClinicalDataProcessor, ClinicalDataGUI

class TestClinicalDataProcessor(unittest.TestCase):
    def setUp(self):
        self.test_host = "test.ftp.com"
        self.test_user = "testuser"
        self.test_pass = "testpass"
        self.processor = ClinicalDataProcessor(self.test_host, self.test_user, self.test_pass)
    
    @patch('ftplib.FTP')
    def test_connect_success(self, mock_ftp_class):
        mock_ftp = MagicMock()
        mock_ftp_class.return_value = mock_ftp
        
        result = self.processor.connect()
        
        self.assertTrue(result)
        self.assertTrue(self.processor.connected)
        mock_ftp_class.assert_called_once_with(self.test_host, timeout=30)
        mock_ftp.login.assert_called_once_with(self.test_user, self.test_pass)
    
    @patch('ftplib.FTP')
    def test_connect_failure(self, mock_ftp_class):
        mock_ftp_class.side_effect = Exception("Connection failed")
        
        result = self.processor.connect()
        
        self.assertFalse(result)
        self.assertFalse(self.processor.connected)
    
    def test_disconnect(self):
        self.processor.ftp = MagicMock()
        self.processor.connected = True
        
        self.processor.disconnect()
        
        self.processor.ftp.quit.assert_called_once()
        self.assertFalse(self.processor.connected)

class TestClinicalDataValidator(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.download_dir = Path(self.temp_dir) / "downloads"
        self.archive_dir = Path(self.temp_dir) / "archive"
        self.error_dir = Path(self.temp_dir) / "errors"
        
        self.validator = ClinicalDataValidator(
            self.download_dir,
            self.archive_dir,
            self.error_dir
        )
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_filename_validation_valid(self):
        valid_filenames = [
            "CLINICALDATA_20231225120000.CSV",
            "clinicaldata_20231225120000.csv",
            "CLINICALDATA_20240101123045.CSV"
        ]
        
        for filename in valid_filenames:
            with self.subTest(filename=filename):
                result = self.validator._validate_filename_pattern(filename)
                self.assertTrue(result)
    
    def test_filename_validation_invalid(self):
        invalid_filenames = [
            "clinical_data_20231225.csv",
            "CLINICALDATA_20231225.CSV",  
            "CLINICALDATA_20231225120000.txt",  
            "test.csv",
            ""
        ]
        
        for filename in invalid_filenames:
            with self.subTest(filename=filename):
                result = self.validator._validate_filename_pattern(filename)
                self.assertFalse(result)
    
    def test_csv_validation_valid(self):
        csv_content = """PatientID,TrialCode,DrugCode,Dosage_mg,StartDate,EndDate,Outcome,SideEffects,Analyst
P001,T001,D001,100,2023-01-01,2023-06-01,Improved,None,John Doe
P002,T001,D002,200,2023-02-01,2023-07-01,No Change,Fatigue,Jane Smith"""
        
        csv_path = self.download_dir / "test.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_path.write_text(csv_content)
        
        is_valid, errors, record_count = self.validator._validate_csv_content(csv_path)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        self.assertEqual(record_count, 2)
    
    def test_csv_validation_invalid_header(self):
        csv_content = """ID,Code,Drug,Dosage,Start,End,Result,SideEffects,Analyst
P001,T001,D001,100,2023-01-01,2023-06-01,Improved,None,John Doe"""
        
        csv_path = self.download_dir / "test.csv"
        csv_path.write_text(csv_content)
        
        is_valid, errors, record_count = self.validator._validate_csv_content(csv_path)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("Invalid header", errors[0])
    
    def test_csv_validation_invalid_dosage(self):
        csv_content = """PatientID,TrialCode,DrugCode,Dosage_mg,StartDate,EndDate,Outcome,SideEffects,Analyst
P001,T001,D001,abc,2023-01-01,2023-06-01,Improved,None,John Doe"""  
        
        csv_path = self.download_dir / "test.csv"
        csv_path.write_text(csv_content)
        
        is_valid, errors, record_count = self.validator._validate_csv_content(csv_path)
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        self.assertIn("Non-numeric dosage", errors[0])
    
    @patch('requests.get')
    def test_generate_guid_api_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = ["123e4567-e89b-12d3-a456-426614174000"]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        guid = self.validator._generate_guid()
        
        self.assertEqual(guid, "123e4567-e89b-12d3-a456-426614174000")
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_generate_guid_api_fallback(self, mock_get):
        mock_get.side_effect = Exception("API failure")
        
        guid = self.validator._generate_guid()
        
        self.assertIsNotNone(guid)
        self.assertIsInstance(guid, str)
        self.assertGreater(len(guid), 0)

class TestClinicalDataGUI(unittest.TestCase):
    
    def setUp(self):
        self.mock_root = Mock(spec=tk.Tk)
        
        with patch('tkinter.Tk', return_value=self.mock_root):
            self.gui = ClinicalDataGUI(self.mock_root)