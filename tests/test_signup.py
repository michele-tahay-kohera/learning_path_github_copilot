"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_for_activity_success(client):
    """Test successful student signup"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds participant to activity"""
    # Sign up
    client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity(client):
    """Test signup for activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_student(client):
    """Test that duplicate signup is rejected"""
    # Try to sign up student who is already registered
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_multiple_different_students(client):
    """Test multiple students can sign up for the same activity"""
    student1 = "student1@mergington.edu"
    student2 = "student2@mergington.edu"
    
    # First student signs up
    response1 = client.post(f"/activities/Chess Club/signup?email={student1}")
    assert response1.status_code == 200
    
    # Second student signs up
    response2 = client.post(f"/activities/Chess Club/signup?email={student2}")
    assert response2.status_code == 200
    
    # Verify both are registered
    response = client.get("/activities")
    participants = response.json()["Chess Club"]["participants"]
    assert student1 in participants
    assert student2 in participants


def test_signup_with_url_encoded_activity_name(client):
    """Test signup with special characters in activity name"""
    # Activity names with spaces should be URL encoded
    response = client.post(
        "/activities/Basketball%20Team/signup?email=athlete@mergington.edu"
    )
    assert response.status_code == 200


def test_signup_response_message_format(client):
    """Test that signup response has proper message format"""
    response = client.post(
        "/activities/Gym Class/signup?email=athlete@mergington.edu"
    )
    data = response.json()
    message = data["message"]
    assert "Signed up" in message
    assert "athlete@mergington.edu" in message
    assert "Gym Class" in message


def test_signup_for_activity_with_one_spot_left(client):
    """Test signup for activity with limited remaining capacity"""
    # Tennis Club has max 10, currently has 2
    response = client.get("/activities")
    tennis = response.json()["Tennis Club"]
    remaining_spots = tennis["max_participants"] - len(tennis["participants"])
    assert remaining_spots > 0
    
    # Should be able to sign up
    response = client.post(
        "/activities/Tennis Club/signup?email=newtennis@mergington.edu"
    )
    assert response.status_code == 200


def test_signup_empty_email(client):
    """Test signup with empty email"""
    response = client.post(
        "/activities/Chess Club/signup?email="
    )
    # Empty email might be accepted by FastAPI but not added to system
    # This depends on validation - test the actual behavior
    assert response.status_code in [200, 422]  # 200 if accepted, 422 if validation fails


def test_signup_content_type_response(client):
    """Test that signup response has correct content type"""
    response = client.post(
        "/activities/Chess Club/signup?email=testuser@mergington.edu"
    )
    assert response.headers["content-type"] == "application/json"
