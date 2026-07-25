from datetime import date, timedelta


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


def test_create_task_blank_tag_among_valid_tags_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["bug", ""]},
    )

    assert response.status_code == 422


def test_create_task_whitespace_only_tag_among_valid_tags_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["bug", "   "]},
    )

    assert response.status_code == 422


def test_create_task_single_blank_tag_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": [""]},
    )

    assert response.status_code == 422


def test_create_task_single_whitespace_only_tag_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Task", "tags": ["   "]},
    )

    assert response.status_code == 422


def test_create_task_with_empty_tags_list_returns_201(client):
    response = client.post("/tasks", json={"title": "Task", "tags": []})

    assert response.status_code == 201
    assert response.json()["tags"] == []


def test_create_task_with_padded_tag_returns_201_and_stores_trimmed_tag(client):
    response = client.post("/tasks", json={"title": "Task", "tags": [" bug "]})

    assert response.status_code == 201
    assert response.json()["tags"] == ["bug"]


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


def test_patch_blank_tag_among_valid_tags_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with tags", "tags": ["backend"]},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": ["backend", ""]})

    assert response.status_code == 422


def test_patch_whitespace_only_tag_among_valid_tags_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with tags", "tags": ["backend"]},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": ["backend", "   "]})

    assert response.status_code == 422


def test_patch_rejected_blank_tag_leaves_stored_tags_unchanged(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with tags", "tags": ["backend"]},
    )
    task_id = create_response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json={"tags": ["backend", ""]})
    assert patch_response.status_code == 422

    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.json()["tags"] == ["backend"]


def test_patch_valid_tags_updates_and_normalizes_stored_tags(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with tags", "tags": ["backend"]},
    )
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": [" Frontend ", "frontend"]})

    assert response.status_code == 200
    assert response.json()["tags"] == ["Frontend"]


def test_list_tasks_overdue_true_returns_overdue_unfinished_task(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    create_response = client.post(
        "/tasks",
        json={"title": "Overdue task", "due_date": yesterday},
    )
    overdue_task = create_response.json()

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == overdue_task["id"]


def test_list_tasks_overdue_true_excludes_future_task(client):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Future task", "due_date": tomorrow})

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_overdue_true_excludes_task_due_today(client):
    today = date.today().isoformat()
    client.post("/tasks", json={"title": "Due today", "due_date": today})

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_overdue_true_excludes_task_without_due_date(client):
    client.post("/tasks", json={"title": "No due date"})

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_overdue_true_excludes_done_task_with_past_due_date(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    create_response = client.post(
        "/tasks",
        json={"title": "Overdue but done", "status": "InProgress", "due_date": yesterday},
    )
    task_id = create_response.json()["id"]
    client.patch(f"/tasks/{task_id}", json={"status": "Done"})

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_without_overdue_param_returns_all_tasks(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Overdue task", "due_date": yesterday})
    client.post("/tasks", json={"title": "Future task", "due_date": tomorrow})
    client.post("/tasks", json={"title": "No due date task"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_tasks_status_and_priority_filters_still_work_with_overdue_param_absent(client, created_task):
    client.post("/tasks", json={"title": "High prio todo", "priority": "High"})

    status_response = client.get("/tasks", params={"status": "ToDo"})
    priority_response = client.get("/tasks", params={"priority": "High"})

    assert status_response.status_code == 200
    assert len(status_response.json()) == 2

    assert priority_response.status_code == 200
    priority_body = priority_response.json()
    assert len(priority_body) == 1
    assert priority_body[0]["priority"] == "High"


def test_list_tasks_overdue_false_excludes_unfinished_task_with_past_due_date(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Overdue task", "due_date": yesterday})

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_overdue_false_includes_future_task(client):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    create_response = client.post("/tasks", json={"title": "Future task", "due_date": tomorrow})
    future_task = create_response.json()

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == future_task["id"]


def test_list_tasks_overdue_false_includes_task_due_today(client):
    today = date.today().isoformat()
    create_response = client.post("/tasks", json={"title": "Due today", "due_date": today})
    due_today_task = create_response.json()

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == due_today_task["id"]


def test_list_tasks_overdue_false_includes_task_without_due_date(client):
    create_response = client.post("/tasks", json={"title": "No due date"})
    no_due_date_task = create_response.json()

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == no_due_date_task["id"]


def test_list_tasks_overdue_false_includes_done_task_with_past_due_date(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    create_response = client.post(
        "/tasks",
        json={"title": "Overdue but done", "status": "InProgress", "due_date": yesterday},
    )
    task_id = create_response.json()["id"]
    done_task = client.patch(f"/tasks/{task_id}", json={"status": "Done"}).json()

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == done_task["id"]


def test_list_tasks_overdue_false_combined_with_status_filter(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Overdue todo", "due_date": yesterday})
    future_response = client.post("/tasks", json={"title": "Future todo", "due_date": tomorrow})
    future_task = future_response.json()

    response = client.get("/tasks", params={"overdue": "false", "status": "ToDo"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == future_task["id"]


def test_list_tasks_overdue_false_combined_with_priority_filter(client):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    high_response = client.post(
        "/tasks",
        json={"title": "Future high prio", "priority": "High", "due_date": tomorrow},
    )
    high_task = high_response.json()
    client.post(
        "/tasks",
        json={"title": "Future low prio", "priority": "Low", "due_date": tomorrow},
    )

    response = client.get("/tasks", params={"overdue": "false", "priority": "High"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == high_task["id"]


def test_list_tasks_filter_by_tag_returns_only_matching_tasks(client):
    urgent_response = client.post("/tasks", json={"title": "Urgent task", "tags": ["urgent"]})
    urgent_task = urgent_response.json()
    client.post("/tasks", json={"title": "Other task", "tags": ["backend"]})

    response = client.get("/tasks", params={"tag": "urgent"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == urgent_task["id"]


def test_list_tasks_filter_by_tag_is_case_insensitive(client):
    create_response = client.post("/tasks", json={"title": "Urgent task", "tags": ["Urgent"]})
    urgent_task = create_response.json()

    response = client.get("/tasks", params={"tag": "URGENT"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == urgent_task["id"]


def test_list_tasks_filter_by_tag_ignores_query_whitespace(client):
    create_response = client.post("/tasks", json={"title": "Urgent task", "tags": ["urgent"]})
    urgent_task = create_response.json()

    response = client.get("/tasks", params={"tag": "  urgent  "})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == urgent_task["id"]


def test_list_tasks_filter_by_tag_does_not_substring_match(client):
    client.post("/tasks", json={"title": "Not urgent task", "tags": ["not-urgent"]})

    response = client.get("/tasks", params={"tag": "urgent"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_tag_excludes_tasks_without_tags(client):
    client.post("/tasks", json={"title": "No tags task"})

    response = client.get("/tasks", params={"tag": "urgent"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_nonexistent_tag_returns_200_and_empty_list(client, created_task):
    response = client.get("/tasks", params={"tag": "does-not-exist"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_without_tag_param_preserves_normal_list_behavior(client):
    client.post("/tasks", json={"title": "Tagged task", "tags": ["urgent"]})
    client.post("/tasks", json={"title": "Untagged task"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_tasks_filter_by_tag_and_status_uses_and_behavior(client):
    matching_response = client.post(
        "/tasks",
        json={"title": "Urgent todo", "status": "ToDo", "tags": ["urgent"]},
    )
    matching_task = matching_response.json()
    client.post(
        "/tasks",
        json={"title": "Urgent in progress", "status": "InProgress", "tags": ["urgent"]},
    )
    client.post("/tasks", json={"title": "Todo no tag", "status": "ToDo"})

    response = client.get("/tasks", params={"tag": "urgent", "status": "ToDo"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == matching_task["id"]


def test_list_tasks_filter_by_tag_and_priority_uses_and_behavior(client):
    matching_response = client.post(
        "/tasks",
        json={"title": "Urgent high prio", "priority": "High", "tags": ["urgent"]},
    )
    matching_task = matching_response.json()
    client.post(
        "/tasks",
        json={"title": "Urgent low prio", "priority": "Low", "tags": ["urgent"]},
    )
    client.post("/tasks", json={"title": "High prio no tag", "priority": "High"})

    response = client.get("/tasks", params={"tag": "urgent", "priority": "High"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == matching_task["id"]


def test_list_tasks_filter_by_tag_and_overdue_true_uses_and_behavior(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    matching_response = client.post(
        "/tasks",
        json={"title": "Urgent overdue", "due_date": yesterday, "tags": ["urgent"]},
    )
    matching_task = matching_response.json()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    client.post(
        "/tasks",
        json={"title": "Urgent future", "due_date": tomorrow, "tags": ["urgent"]},
    )
    client.post("/tasks", json={"title": "Overdue no tag", "due_date": yesterday})

    response = client.get("/tasks", params={"tag": "urgent", "overdue": "true"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == matching_task["id"]
