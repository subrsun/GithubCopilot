"""
Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all activities with correct structure.

        Arrange: No setup needed (activities fixture handles initial state)
        Act: Make GET request to /activities
        Assert: Verify all activities are returned with expected structure
        """
        # Arrange
        expected_activity_count = 9
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swimming Club",
            "Art Club",
            "Drama Club",
            "Science Club",
            "Debate Team"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == expected_activity_count
        assert set(data.keys()) == set(expected_activities)

    def test_activity_has_required_fields(self, client):
        """
        Test that each activity has all required fields.

        Arrange: No setup needed
        Act: Get activities and check first activity structure
        Assert: Verify required fields exist
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()
        first_activity = data["Chess Club"]

        # Assert
        assert set(first_activity.keys()) == required_fields

    def test_activity_participants_is_list(self, client):
        """
        Test that participants field is a list of email addresses.

        Arrange: No setup needed
        Act: Get activities
        Assert: Verify participants field is a list with email strings
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation

    def test_activity_has_valid_max_participants(self, client):
        """
        Test that max_participants is a positive integer.

        Arrange: No setup needed
        Act: Get activities
        Assert: Verify max_participants is a positive integer
        """
        # Arrange
        # (no setup needed)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0
