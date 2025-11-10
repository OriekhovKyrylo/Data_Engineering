"""
Tests for sales_api data access layer
"""
import os
from unittest.mock import patch, Mock
import pytest

from lec02.job1.dal.sales_api import get_sales


class TestGetSales:
    """Tests for get_sales function"""

    @patch('lec02.job1.dal.sales_api.requests.get')
    def test_get_sales_success_single_page(self, mock_get: Mock) -> None:
        """Test successful data retrieval with single page"""
        # Arrange
        os.environ['AUTH_TOKEN'] = 'test_token'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [{'client': 'John', 'product': 'Apple', 'price': 100}],
            []  # Empty response to stop pagination
        ]
        mock_get.return_value = mock_response

        # Act
        result = get_sales(date='2022-08-09')

        # Assert
        assert len(result) == 1
        assert result[0]['client'] == 'John'
        assert mock_get.call_count == 2

    @patch('lec02.job1.dal.sales_api.requests.get')
    def test_get_sales_success_multiple_pages(self, mock_get: Mock) -> None:
        """Test successful data retrieval with multiple pages"""
        # Arrange
        os.environ['AUTH_TOKEN'] = 'test_token'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            [{'client': 'John', 'product': 'Apple', 'price': 100}],
            [{'client': 'Jane', 'product': 'Banana', 'price': 50}],
            []
        ]
        mock_get.return_value = mock_response

        # Act
        result = get_sales(date='2022-08-09')

        # Assert
        assert len(result) == 2
        assert result[0]['client'] == 'John'
        assert result[1]['client'] == 'Jane'

    def test_get_sales_no_auth_token(self) -> None:
        """Test error when AUTH_TOKEN is not set"""
        # Arrange
        if 'AUTH_TOKEN' in os.environ:
            del os.environ['AUTH_TOKEN']

        # Act & Assert
        with pytest.raises(ValueError, match="AUTH_TOKEN environment variable is not set"):
            get_sales(date='2022-08-09')

    @patch('lec02.job1.dal.sales_api.requests.get')
    def test_get_sales_api_error(self, mock_get: Mock) -> None:
        """Test handling API error response"""
        # Arrange
        os.environ['AUTH_TOKEN'] = 'test_token'
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_get.return_value = mock_response

        # Act
        result = get_sales(date='2022-08-09')

        # Assert
        assert result == []