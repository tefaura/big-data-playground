"""Unit tests for get_data.py pipeline script."""

import pytest
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import sys
import importlib.util

# Import get_data module from scripts directory
scripts_dir = Path(__file__).parent.parent / "scripts"
spec = importlib.util.spec_from_file_location("get_data", scripts_dir / "get_data.py")
get_data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(get_data)

ingest_raw_csv = get_data.ingest_raw_csv
build_curated_parquet = get_data.build_curated_parquet
main = get_data.main


class TestIngestRawCsv:
    """Tests for ingest_raw_csv function."""
    
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    @patch('pathlib.Path.mkdir')
    def test_ingest_raw_csv_from_url(self, mock_mkdir, mock_to_csv, mock_read_csv, tmp_path):
        """Test ingesting CSV from URL."""
        # Setup
        source = "https://example.com/data.csv"
        raw_path = tmp_path / "raw" / "data.csv"
        test_df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        mock_read_csv.return_value = test_df
        
        # Execute
        ingest_raw_csv(source, raw_path)
        
        # Assert
        mock_read_csv.assert_called_once_with(source)
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_to_csv.assert_called_once_with(raw_path, index=False)
    
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    @patch('pathlib.Path.mkdir')
    def test_ingest_raw_csv_creates_directory(self, mock_mkdir, mock_to_csv, mock_read_csv, tmp_path):
        """Test that parent directories are created."""
        source = "test.csv"
        raw_path = tmp_path / "new" / "dir" / "data.csv"
        test_df = pd.DataFrame({"col1": [1, 2]})
        mock_read_csv.return_value = test_df
        
        ingest_raw_csv(source, raw_path)
        
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_to_csv.assert_called_once_with(raw_path, index=False)
    
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    @patch('pathlib.Path.mkdir')
    def test_ingest_raw_csv_saves_correct_data(self, mock_mkdir, mock_to_csv, mock_read_csv, tmp_path):
        """Test that CSV is saved with correct data."""
        source = "test.csv"
        raw_path = tmp_path / "data.csv"
        test_df = pd.DataFrame({"id": [1, 2, 3], "name": ["A", "B", "C"]})
        mock_read_csv.return_value = test_df
        
        ingest_raw_csv(source, raw_path)
        
        # Verify the file would be written (using to_csv)
        mock_read_csv.assert_called_once_with(source)
        mock_to_csv.assert_called_once_with(raw_path, index=False)


class TestBuildCuratedParquet:
    """Tests for build_curated_parquet function."""
    
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_parquet')
    @patch('pathlib.Path.mkdir')
    def test_build_curated_parquet_converts_csv_to_parquet(self, mock_mkdir, mock_to_parquet, mock_read_csv, tmp_path):
        """Test converting CSV to Parquet format."""
        raw_path = tmp_path / "raw.csv"
        curated_path = tmp_path / "curated.parquet"
        test_df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4.5, 5.6, 6.7]})
        mock_read_csv.return_value = test_df
        
        build_curated_parquet(raw_path, curated_path)
        
        mock_read_csv.assert_called_once_with(raw_path)
        mock_to_parquet.assert_called_once_with(curated_path, index=False, engine="pyarrow")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
    
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_parquet')
    @patch('pathlib.Path.mkdir')
    def test_build_curated_parquet_creates_directory(self, mock_mkdir, mock_to_parquet, mock_read_csv, tmp_path):
        """Test that parent directories are created."""
        raw_path = tmp_path / "raw.csv"
        curated_path = tmp_path / "new" / "dir" / "curated.parquet"
        test_df = pd.DataFrame({"col1": [1]})
        mock_read_csv.return_value = test_df
        
        build_curated_parquet(raw_path, curated_path)
        
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)


class TestMain:
    """Tests for main function."""
    
    @patch.object(get_data, 'build_curated_parquet')
    @patch.object(get_data, 'ingest_raw_csv')
    def test_main_with_default_paths(self, mock_ingest, mock_build):
        """Test main function with default output paths."""
        test_args = [
            "get_data.py",
            "--source",
            "https://example.com/data.csv"
        ]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_ingest.assert_called_once()
        mock_build.assert_called_once()
        
        # Check that ingest was called with correct source
        assert mock_ingest.call_args[0][0] == "https://example.com/data.csv"
    
    @patch.object(get_data, 'build_curated_parquet')
    @patch.object(get_data, 'ingest_raw_csv')
    def test_main_with_custom_paths(self, mock_ingest, mock_build):
        """Test main function with custom output paths."""
        test_args = [
            "get_data.py",
            "--source",
            "test.csv",
            "--raw-out",
            "custom/raw.csv",
            "--curated-out",
            "custom/curated.parquet"
        ]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_ingest.assert_called_once()
        mock_build.assert_called_once()
        
        # Verify paths
        ingest_call = mock_ingest.call_args
        assert str(ingest_call[0][1]) == "custom/raw.csv"
        
        build_call = mock_build.call_args
        assert str(build_call[0][1]) == "custom/curated.parquet"
    
    def test_main_requires_source_argument(self):
        """Test that main requires --source argument."""
        test_args = ["get_data.py"]
        
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit):
                main()

