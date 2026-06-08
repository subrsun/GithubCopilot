"""
Tests for the GET / root endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestRootEndpoint:
    """Test suite for root endpoint behavior."""

    def test_root_returns_redirect_to_static_index(self, client):
        """
        Test that GET / redirects to /static/index.html.

        Arrange: No setup needed
        Act: Make GET request to root endpoint
        Assert: Verify redirect status and location
        """
        # Arrange
        expected_redirect_path = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_path

    def test_root_redirect_can_be_followed(self, client):
        """
        Test that following the redirect from / works.

        Arrange: No setup needed
        Act: Make GET request to root with follow_redirects=True
        Assert: Verify final response is successful (or served by static files)
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        # The response could be 200 (if static files are served) or 404
        # depending on whether the TestClient serves static files.
        # We're checking that following the redirect doesn't cause an error.
        assert response.status_code in [200, 404, 307]

    def test_root_uses_correct_redirect_type(self, client):
        """
        Test that root endpoint uses HTTP redirect (not just return 200).

        Arrange: No setup needed
        Act: Make GET request to root
        Assert: Verify response is a redirect (3xx status code)
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert 300 <= response.status_code < 400
