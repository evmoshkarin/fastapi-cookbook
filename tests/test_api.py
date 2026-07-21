def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Добро пожаловать в Кулинарную книгу API!",
        "recipe_id": None,
    }


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "API работает нормально", "recipe_id": None}


def test_create_recipe(client):
    payload = {
        "title": "Тестовый рецепт",
        "cooking_time": 30,
        "ingredients": ["ингредиент1", "ингредиент2"],
        "description": "Описание тестового рецепта",
    }
    response = client.post("/recipes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Рецепт 'Тестовый рецепт' успешно создан"
    assert data["recipe_id"] is not None


def test_get_recipe_list(client):
    payload = {
        "title": "Рецепт для списка",
        "cooking_time": 15,
        "ingredients": ["a", "b"],
        "description": "desc",
    }
    client.post("/recipes", json=payload)

    response = client.get("/recipes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_recipe_detail(client):
    payload = {
        "title": "Детальный рецепт",
        "cooking_time": 20,
        "ingredients": ["x", "y"],
        "description": "описание",
    }
    create_resp = client.post("/recipes", json=payload)
    recipe_id = create_resp.json()["recipe_id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["title"] == "Детальный рецепт"
    assert "ingredients" in data
    assert isinstance(data["ingredients"], list)


def test_get_nonexistent_recipe(client):
    response = client.get("/recipes/9999")
    assert response.status_code == 404
    assert "не найден" in response.json()["detail"]
