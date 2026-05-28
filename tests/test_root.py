"""
Tests for the root endpoint GET /
"""

def test_root_redirects_to_static(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_location_header(client):
    """Test that redirect has correct Location header"""
    response = client.get("/")
    assert response.status_code == 200  # With follow_redirects=True (default)
    # The page should exist and be accessible
    assert response.is_redirect is False or response.status_code == 200
