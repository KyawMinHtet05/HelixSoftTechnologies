import pytest
import uuid
from unittest.mock import patch, Mock
import requests

from HelixSoftTechnologies import ClinicalDataValidator

@pytest.fixture
def temp_validator(tmp_path):
    return ClinicalDataValidator(
        tmp_path / "download",
        tmp_path / "archive", 
        tmp_path / "error"
    )

class TestGenerateGUID:
    
    def test_api_timeout_fallback(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout
            
            result = temp_validator._generate_guid()
            
            assert isinstance(result, str)
            assert len(result) == 36  
            assert result.count('-') == 4
    
    def test_api_connection_error_fallback(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError
            
            result = temp_validator._generate_guid()
            
            assert len(result) == 36
            assert result.count('-') == 4
    
    def test_api_http_error_fallback(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
            
            mock_get.return_value = mock_response
            
            result = temp_validator._generate_guid()
            
            assert len(result) == 36
    
    def test_api_returns_empty_list(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []  
            mock_get.return_value = mock_response
            
            result = temp_validator._generate_guid()
            
            assert len(result) == 36
    
    def test_api_returns_wrong_format(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"wrong": "format"}  
            mock_get.return_value = mock_response
            
            result = temp_validator._generate_guid()
            
            assert len(result) == 36
    
    def test_api_returns_invalid_json(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_get.return_value = mock_response
            
            result = temp_validator._generate_guid()
            
            assert len(result) == 36
    
    def test_local_uuid_is_valid_format(self, temp_validator):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Any error")
            
            result = temp_validator._generate_guid()
            
            parsed_uuid = uuid.UUID(result)
            assert parsed_uuid.version == 4  


def test_guid_in_error_logging(temp_validator, tmp_path):
    test_guid = "test-guid-12345"
    
    with patch.object(temp_validator, '_generate_guid', return_value=test_guid):
        guid, log_entry = temp_validator._log_error(
            "CLINICALDATA_20240101120000.CSV",
            "Test validation error"
        )
        
        assert guid == test_guid
        assert f"GUID: {test_guid}" in log_entry
        assert "File: CLINICALDATA_20240101120000.CSV" in log_entry
        assert "Error: Test validation error" in log_entry