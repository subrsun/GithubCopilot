"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint using AAA pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities."""

    def test_unregister_successful_removes_student(self, client):
        """
        Test successful unregistration of student from activity.

        Arrange: Student already in Chess Club (from fixtures)
        Act: Make DELETE request to unregister endpoint
        Assert: Verify student is removed and success message returned
        """
        # Arrange
        activity_name = "Chess Club"
        student = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Unregistered {student}" in data["message"]

    def test_unregister_actually_removes_from_participants(self, client):
        """
        Test that unregister actually removes student from participants list.

        Arrange: Student initially in Programming Class
        Act: Unregister student and retrieve activities
        Assert: Verify student no longer in participants list
        """
        # Arrange
        activity_name = "Programming Class"
        student = "emma@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert student not in activities_data[activity_name]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Test that unregistering from non-existent activity returns 404.

        Arrange: Prepare non-existent activity name and student email
        Act: Make DELETE request to unregister endpoint
        Assert: Verify 404 status and appropriate error message
        """
        # Arrange
        nonexistent_activity = "Medieval Jousting"
        student = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": student}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_student_not_signed_up_returns_400(self, client):
        """
        Test that unregistering student not in activity returns 400 error.

        Arrange: Student not in Gym Class (from fixtures)
        Act: Attempt to unregister student from Gym Class
        Assert: Verify 400 status and not signed up error message
        """
        # Arrange
        activity_name = "Gym Class"
        student_not_signed_up = "nosignup@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_not_signed_up}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_unregister_returns_correct_message_format(self, client):
        """
        Test that unregister returns message with correct email and activity name.

        Arrange: Student in Debate Team
        Act: Unregister student
        Assert: Verify response message contains both email and activity name
        """
        # Arrange
        activity_name = "Debate Team"
        student = "oliver@mergington.edu"
        expected_message = f"Unregistered {student} from {activity_name}"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message

    def test_unregister_one_student_leaves_others(self, client):
        """
        Test that unregistering one student leaves other participants intact.

        Arrange: Multiple students in Art Club
        Act: Unregister one student
        Assert: Verify other students remain in participants list
        """
        # Arrange
        activity_name = "Art Club"
        student_to_remove = "lily@mergington.edu"
        student_to_keep = "james@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student_to_remove}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert student_to_remove not in activities_data[activity_name]["participants"]
        assert student_to_keep in activities_data[activity_name]["participants"]

    def test_unregister_cannot_unregister_twice(self, client):
        """
        Test that unregistering same student twice returns error on second attempt.

        Arrange: Student in Drama Club
        Act: Unregister student first time (should succeed), then try again
        Assert: Verify first succeeds, second returns 400
        """
        # Arrange
        activity_name = "Drama Club"
        student = "sarah@mergington.edu"

        # Act
        first_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student}
        )
        second_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": student}
        )

        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 400
        assert "not signed up" in second_response.json()["detail"]
