"""
Tests for local_disk data access layer
"""
import os
import json
import tempfile
import shutil
from typing import List, Dict, Any

import pytest

from lec02.job1.dal.local_disk import save_to_disk


class TestSaveToDisk:
    """Tests for save_to_disk function"""

    def setup_method(self) -> None:
        """Setup test fixtures"""
        self.test_dir = tempfile.mkdtemp()

    def teardown_method(self) -> None:
        """Cleanup test fixtures"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_to_disk_success(self) -> None:
        """Test successful save to disk"""
        # Arrange
        test_data: List[Dict[str, Any]] = [
            {'client': 'John', 'product': 'Apple', 'price': 100}
        ]
        test_path = os.path.join(self.test_dir, 'raw', 'sales', '2022-08-09')

        # Act
        save_to_disk(test_data, test_path)

        # Assert
        assert os.path.exists(test_path)
        expected_file = os.path.join(test_path, 'sales_2022-08-09.json')
        assert os.path.exists(expected_file)

        with open(expected_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        assert saved_data == test_data

    def test_save_to_disk_idempotency(self) -> None:
        """Test that save_to_disk is idempotent"""
        # Arrange
        test_data_1: List[Dict[str, Any]] = [
            {'client': 'John', 'product': 'Apple', 'price': 100}
        ]
        test_data_2: List[Dict[str, Any]] = [
            {'client': 'Jane', 'product': 'Banana', 'price': 50}
        ]
        test_path = os.path.join(self.test_dir, 'raw', 'sales', '2022-08-09')

        # Act
        save_to_disk(test_data_1, test_path)
        save_to_disk(test_data_2, test_path)

        # Assert
        expected_file = os.path.join(test_path, 'sales_2022-08-09.json')
        with open(expected_file, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        assert saved_data == test_data_2  # Should contain only second data

    def test_save_to_disk_creates_directory(self) -> None:
        """Test that directory is created if not exists"""
        # Arrange
        test_data: List[Dict[str, Any]] = [
            {'client': 'John', 'product': 'Apple', 'price': 100}
        ]
        test_path = os.path.join(self.test_dir, 'new_dir', 'sales', '2022-08-09')

        # Act
        save_to_disk(test_data, test_path)

        # Assert
        assert os.path.exists(test_path)