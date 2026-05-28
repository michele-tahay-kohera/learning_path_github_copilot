"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint
"""


def test_unregister_success(client):
    """Test successful student unregistration"""
    # Unregister a student who is registered
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes participant from activity"""
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    
    # Verify participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregister from activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_student_not_registered(client):
    """Test that unregistering a student not in activity fails"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notstudent@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_multiple_participants(client):
    """Test unregistering multiple participants sequentially"""
    # Chess Club has 2 initial participants
    response = client.get("/activities")
    initial_count = len(response.json()["Chess Club"]["participants"])
    assert initial_count == 2
    
    # Unregister first participant
    client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    
    # Verify count decreased
    response = client.get("/activities")
    after_first = len(response.json()["Chess Club"]["participants"])
    assert after_first == 1
    
    # Unregister second participant
    client.delete(
        "/activities/Chess Club/unregister?email=daniel@mergington.edu"
    )
    
    # Verify count decreased again
    response = client.get("/activities")
    after_second = len(response.json()["Chess Club"]["participants"])
    assert after_second == 0


def test_unregister_with_url_encoded_activity_name(client):
    """Test unregister with special characters in activity name"""
    response = client.delete(
        "/activities/Basketball%20Team/unregister?email=james@mergington.edu"
    )
    assert response.status_code == 200


def test_unregister_response_message_format(client):
    """Test that unregister response has proper message format"""
    response = client.delete(
        "/activities/Gym Class/unregister?email=john@mergington.edu"
    )
    data = response.json()
    message = data["message"]
    assert "Unregistered" in message
    assert "john@mergington.edu" in message
    assert "Gym Class" in message


def test_unregister_content_type_response(client):
    """Test that unregister response has correct content type"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.headers["content-type"] == "application/json"


def test_unregister_then_signup_again(client):
    """Test that student can sign up again after unregistering"""
    student = "michael@mergington.edu"
    
    # Unregister
    client.delete(f"/activities/Chess Club/unregister?email={student}")
    
    # Verify removed
    response = client.get("/activities")
    assert student not in response.json()["Chess Club"]["participants"]
    
    # Sign up again
    response = client.post(f"/activities/Chess Club/signup?email={student}")
    assert response.status_code == 200
    
    # Verify added back
    response = client.get("/activities")
    assert student in response.json()["Chess Club"]["participants"]
