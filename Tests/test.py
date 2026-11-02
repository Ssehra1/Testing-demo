def test_create_and_fetch_item(client):
    # Step 1: Create an item through the API
    created = client.post(
        "/items",
        json={"name": "keyboard"}
    )
    assert created.status_code == 201
    assert created.json == {
        "id": 1,
        "name": "keyboard"
    }

    # Step 2: Retrieve the item through the API
    fetched = client.get("/items/1")
    assert fetched.status_code == 200
    assert fetched.json["name"] == "keyboard"

    # Step 3: Verify actual database persistence
    with psycopg.connect(
        os.environ["DATABASE_URL"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name FROM items WHERE id = 1"
            )
            assert cursor.fetchone() == ("keyboard",)
