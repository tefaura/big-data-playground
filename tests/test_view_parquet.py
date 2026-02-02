"""Unit tests for view_parquet.py script."""

import pytest
from pathlib import Path
from unittest.mock import patch
import pandas as pd
import sys
import importlib.util

# Import view_parquet module from scripts directory
scripts_dir = Path(__file__).parent.parent / "scripts"
spec = importlib.util.spec_from_file_location("view_parquet", scripts_dir / "view_parquet.py")
view_parquet_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(view_parquet_module)

view_parquet = view_parquet_module.view_parquet
main = view_parquet_module.main


class TestViewParquet:
    """Tests for view_parquet function."""
    
    @patch('pandas.read_parquet')
    @patch('pandas.set_option')
    def test_view_parquet_displays_info(self, mock_set_option, mock_read_parquet, tmp_path):
        """Test that view_parquet displays dataset information."""
        parquet_path = tmp_path / "test.parquet"
        test_df = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": ["a", "b", "c"],
            "col3": [1.1, 2.2, None]
        })
        mock_read_parquet.return_value = test_df
        
        with patch('builtins.print') as mock_print:
            view_parquet(parquet_path, num_rows=3)
        
        # Verify parquet was read
        mock_read_parquet.assert_called_once_with(parquet_path)
        
        # Verify pandas display options were set
        assert mock_set_option.call_count == 3
        
        # Verify print was called (checking for key outputs)
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Dataset:" in str(call) for call in mock_print.call_args_list)
        assert any("Shape" in str(call) for call in mock_print.call_args_list)
    
    @patch('pandas.read_parquet')
    @patch('pandas.set_option')
    def test_view_parquet_with_custom_rows(self, mock_set_option, mock_read_parquet, tmp_path):
        """Test view_parquet with custom number of rows."""
        parquet_path = tmp_path / "test.parquet"
        test_df = pd.DataFrame({"col1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        mock_read_parquet.return_value = test_df
        
        with patch('builtins.print') as mock_print:
            view_parquet(parquet_path, num_rows=10)
        
        # Verify parquet was read
        mock_read_parquet.assert_called_once_with(parquet_path)
        # Verify it printed information about 10 rows
        assert mock_print.called
    
    @patch('pandas.read_parquet')
    @patch('pandas.set_option')
    def test_view_parquet_handles_missing_values(self, mock_set_option, mock_read_parquet, tmp_path):
        """Test that view_parquet correctly handles missing values."""
        parquet_path = tmp_path / "test.parquet"
        test_df = pd.DataFrame({
            "col1": [1, None, 3],
            "col2": [None, "b", None]
        })
        mock_read_parquet.return_value = test_df
        
        with patch('builtins.print') as mock_print:
            view_parquet(parquet_path)
        
        # Verify parquet was read and info was printed
        mock_read_parquet.assert_called_once_with(parquet_path)
        assert mock_print.called


class TestMain:
    """Tests for main function."""
    
    @patch.object(view_parquet_module, 'view_parquet')
    def test_main_with_valid_file(self, mock_view, tmp_path):
        """Test main function with valid parquet file."""
        parquet_file = tmp_path / "test.parquet"
        parquet_file.touch()  # Create the file
        
        test_args = [
            "view_parquet.py",
            str(parquet_file)
        ]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_view.assert_called_once()
        assert mock_view.call_args[0][0] == parquet_file
        assert mock_view.call_args[0][1] == 5  # default rows
    
    @patch.object(view_parquet_module, 'view_parquet')
    def test_main_with_custom_rows(self, mock_view, tmp_path):
        """Test main function with custom --rows argument."""
        parquet_file = tmp_path / "test.parquet"
        parquet_file.touch()
        
        test_args = [
            "view_parquet.py",
            str(parquet_file),
            "--rows",
            "10"
        ]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        mock_view.assert_called_once()
        assert mock_view.call_args[0][1] == 10
    
    @patch('builtins.print')
    def test_main_with_nonexistent_file(self, mock_print, tmp_path):
        """Test main function handles nonexistent file gracefully."""
        nonexistent_file = tmp_path / "nonexistent.parquet"
        
        test_args = [
            "view_parquet.py",
            str(nonexistent_file)
        ]
        
        with patch.object(sys, 'argv', test_args):
            main()
        
        # Should print error and return without calling view_parquet
        mock_print.assert_called()
        assert "Error" in str(mock_print.call_args) or "not found" in str(mock_print.call_args).lower()

