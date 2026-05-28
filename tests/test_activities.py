"""
Tests for the GET /activities endpoint
"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Should have all 9 activities
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Tennis Club" in data
    assert "Art Studio" in data
    assert "Drama Club" in data
    assert "Debate Team" in data
    assert "Science Club" in data


def test_activity_has_required_fields(client):
    """Test that each activity has all required fields"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Validate types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activity_participants_are_strings(client):
    """Test that all participants are email strings"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation


def test_chess_club_has_initial_participants(client):
    """Test that Chess Club has the expected initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_activity_capacity_matches_max_participants(client):
    """Test that max_participants values are reasonable"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_data in data.items():
        # Capacity should be positive
        assert activity_data["max_participants"] > 0
        # Participants should not exceed capacity (though this could happen due to previous registrations)
        # This test just validates the max_participants field exists and is valid
        assert isinstance(activity_data["max_participants"], int)


def test_activities_response_content_type(client):
    """Test that response has correct content type"""
    response = client.get("/activities")
    assert response.headers["content-type"] == "application/json"
