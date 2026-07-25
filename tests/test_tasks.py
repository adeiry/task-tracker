def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover the tasks API",
            "status": "ToDo",
            "priority": "High",
            "assignee": "alaa",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover the tasks API"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alaa"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "priority": "Urgent"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "made_up": "value"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    response = client.get("/tasks", params={"status": "Done"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low prio", "priority": "Low"})
    high_response = client.post("/tasks", json={"title": "High prio", "priority": "High"})
    high_task = high_response.json()

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == high_task["id"]
    assert body[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/nonexistent-id")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"description": "updated description"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["description"] == "updated description"
    assert body["title"] == created_task["title"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/nonexistent-id", json={"description": "x"})

    assert response.status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/nonexistent-id")

    assert response.status_code == 404


def test_create_task_with_valid_due_date_returns_201_and_same_iso_date(client):
    response = client.post(
        "/tasks",
        json={"title": "Task with due date", "due_date": "2026-08-01"},
    )

    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-08-01"


def test_create_task_without_due_date_returns_201_with_null_due_date(client):
    response = client.post("/tasks", json={"title": "Task without due date"})

    assert response.status_code == 201
    assert response.json()["due_date"] is None


def test_create_task_invalid_due_date_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "due_date": "not-a-date"},
    )

    assert response.status_code == 422


def test_patch_due_date_updates_existing_task(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-09-15"},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-09-15"


def test_patch_due_date_null_clears_existing_due_date(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with due date", "due_date": "2026-08-01"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"due_date": None})

    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_create_task_with_multiple_tags_returns_201_with_tags(client):
    response = client.post(
        "/tasks",
        json={"title": "Task with tags", "tags": ["Urgent", "Bug"]},
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["Urgent", "Bug"]


def test_create_task_without_tags_returns_201_with_empty_list(client):
    response = client.post("/tasks", json={"title": "Task without tags"})

    assert response.status_code == 201
    assert response.json()["tags"] == []


def test_create_task_empty_tags_are_ignored(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["Urgent", "", "   "]},
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["Urgent"]


def test_create_task_duplicate_tags_are_removed(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["Bug", "bug", "BUG"]},
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["Bug"]


def test_patch_tags_replaces_existing_list(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with tags", "tags": ["a", "b"]},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": ["c"]})

    assert response.status_code == 200
    assert response.json()["tags"] == ["c"]
