import pytest
from datetime import date

from prj import User, Project, Task

class TestTask:
    @pytest.fixture
    def task(self):
        return Task(name="Task1", description="Desc", start_date="2025-01-01", end_date="2025-01-31")

    def test_initial_status_and_performers(self, task):
        assert not task.status
        assert task.performers == []

    def test_change_status(self, task):
        original = task.status
        task.change_status()
        assert task.status != original
        task.change_status()
        assert task.status == original

    def test_add_and_remove_performer(self, task):
        task.add_performer("bob")
        assert "bob" in task.performers
        task.remove_performer("bob")
        assert "bob" not in task.performers
        with pytest.raises(ValueError):
            task.remove_performer("charlie")

    def test_to_dict_and_from_dict(self, task):
        task.change_status()
        task.add_performer("bob")
        data = task.to_dict()
        assert data["name"] == "Task1"
        assert data["status"] is True
        assert "bob" in data["performers"]

        new_task = Task.from_dict(data)
        assert new_task.name == task.name
        assert new_task.description == task.description
        assert new_task.start_date == task.start_date
        assert new_task.end_date == task.end_date
        assert new_task.status == task.status
        assert new_task.performers == task.performers