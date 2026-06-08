"""
Tests for the POST /activities/{activity_name}/signup endpoint using AAA pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""

    def test_signup_successful_new_student(self, client):
        """
        Test successful signup of a new student to an activity.

        Arrange: Prepare email of student not in activity
        Act: Make POST request to signup endpoint
        Assert: Verify student is added and success message returned
        """
        # Arrange
        activity_name = "Chess Club"
        new_student = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {new_student}" in data["message"]

    def test_signup_adds_student_to_participants(self, client):
        """
        Test that signup actually adds student to activity participants.

        Arrange: Prepare email of student not yet in activity
        Act: Sign up student, then retrieve activities
        Assert: Verify student appears in participants list
        """
        # Arrange
        activity_name = "Programming Class"
        new_student = "testuser@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response.status_code == 200
        assert new_student in activities_data[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Test that signing up for non-existent activity returns 404.

        Arrange: Prepare non-existent activity name and student email
        Act: Make POST request to signup endpoint
        Assert: Verify 404 status and appropriate error message
        """
        # Arrange
        nonexistent_activity = "Underwater Basket Weaving"
        student = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": student}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student_returns_400(self, client):
        """
        Test that signing up same student twice returns 400 error.

        Arrange: Student already in Chess Club (from fixtures)
        Act: Attempt to sign up same student again
        Assert: Verify 400 status and duplicate signup error message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_student = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_student}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_returns_correct_message_format(self, client):
        """
        Test that signup returns message with correct email and activity name.

        Arrange: Prepare unique email and activity name
        Act: Sign up student
        Assert: Verify response message contains both email and activity name
        """
        # Arrange
        activity_name = "Art Club"
        student_email = "artist@mergington.edu"
        expected_message = f"Signed up {student_email} for {activity_name}"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == expected_message

    def test_signup_multiple_different_students_same_activity(self, client):
        """
        Test that multiple different students can signup for same activity.

        Arrange: Prepare two different student emails
        Act: Sign up both students for same activity
        Assert: Verify both are successfully added
        """
        # Arrange
        activity_name = "Swimming Club"
        student1 = "student1@mergington.edu"
        student2 = "student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": student2}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert student1 in activities_data[activity_name]["participants"]
        assert student2 in activities_data[activity_name]["participants"]

    def test_signup_same_student_different_activities(self, client):
        """
        Test that same student can signup for multiple different activities.

        Arrange: Prepare student email and multiple activities
        Act: Sign up student for two different activities
        Assert: Verify student is in participants for both activities
        """
        # Arrange
        student = "versatile@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Drama Club"

        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": student}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": student}
        )
        activities_response = client.get("/activities")
        activities_data = activities_response.json()

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert student in activities_data[activity1]["participants"]
        assert student in activities_data[activity2]["participants"]
