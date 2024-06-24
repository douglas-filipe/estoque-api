def test_create_product(test_client):
    category_data = {"description": "Test Category"}
    
    user_data = {
        "email": "test_user@email.com",
        "password": "testpassword",
        "name": "Test User"
    }

    resp_category = test_client.post("/category", json=category_data)
    
    res_user = test_client.post("/user", json=user_data)
    
    category_id = resp_category.json()["id"]
    
    user_id = res_user.json()["id"]
    
    product_data = {
        "description": "Product",
        "price": 100,
        "category_id": category_id,
        "stock_quantity": 100,
        "user_id": user_id
    }
    
    res_product = test_client.post("/product", json=product_data)
    
    assert res_product.status_code == 200