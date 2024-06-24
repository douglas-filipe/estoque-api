def test_create_category(test_client):
    category_data = {"description": "Test Category"}
    
    response = test_client.post("/category", json=category_data)
    
    assert response.status_code == 200
    
    created_category = response.json()
    
    assert "id" in created_category
    assert created_category["description"] == category_data["description"]
    
def test_get_categories(test_client):
    category_data = {"description": "Test Category"}
    response_post = test_client.post("/category", json=category_data)
    assert response_post.status_code == 200
    created_category = response_post.json()
    assert "id" in created_category
    assert created_category["description"] == category_data["description"]

    response_get = test_client.get("/category")
    assert response_get.status_code == 200
    categories = response_get.json()
    
    assert any(category["id"] == created_category["id"] for category in categories)