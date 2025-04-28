import pytest

from prj import User, Project, Task

class TestProject:
    @pytest.fixture
    def project(self):
        return Project(name="Proj1", description="DescProj", start_date="2025-02-01", end_date="2025-12-31")

    @pytest.fixture
    def task1(self):
        return Task(name="T1", description="D1", start_date="2025-03-01", end_date="2025-03-31")

    @pytest.fixture
    def task2(self):
        t = Task(name="T2", description="D2", start_date="2025-04-01", end_date="2025-04-30")
        t.change_status()
        return t

    def test_add_and_remove_task(self, project, task1):
        project.add_task(task1)
        assert task1 in project.tasks
        project.remove_task(task1)
        assert task1 not in project.tasks
        with pytest.raises(ValueError):
            project.remove_task(task1)

    def test_find_task_by_name(self, project, task1, task2):
        project.add_task(task1)
        project.add_task(task2)
        assert project.find_task_by_name("T1") == [task1]
        assert project.find_task_by_name("TX") == []

    def test_find_task_by_start_and_end_date(self, project, task1, task2):
        project.add_task(task1)
        project.add_task(task2)
        assert project.find_task_by_start_date("2025-03-01") == [task1]
        assert project.find_task_by_end_date("2025-04-30") == [task2]
        assert project.find_task_by_start_date("2020-01-01") == []

    def test_is_completed(self, project, task1, task2):
        # no tasks -> vacuously completed
        assert project.is_completed()
        project.add_task(task1)
        # task1.status False -> not completed
        assert not project.is_completed()
        project.add_task(task2)
        # one false, one true -> still not completed
        assert not project.is_completed()
        task1.change_status()
        # now both true -> completed
        assert project.is_completed()

    def test_to_dict_and_from_dict(self, project, task1, task2):
        project.add_task(task1)
        project.add_task(task2)
        data = project.to_dict()
        assert data["name"] == "Proj1"
        assert isinstance(data["tasks"], list)

        new_proj = Project.from_dict(data)
        assert new_proj.name == project.name
        assert new_proj.description == project.description
        assert new_proj.start_date == project.start_date
        assert new_proj.end_date == project.end_date

        assert len(new_proj.tasks) == 2
        names = [t.name for t in new_proj.tasks]
        assert "T1" in names and "T2" in names


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

import pytest

from prj import User

class TestUser:
    @pytest.fixture
    def user(self):
        return User(login="alice", password="secret", role="developer")

    def test_authenticate_success(self, user):
        assert user.authenticate("alice", "secret")

    def test_authenticate_failure(self, user):
        assert not user.authenticate("alice", "wrong")
        assert not user.authenticate("bob", "secret")

    def test_authorize_success(self, user):
        assert user.authorize(["developer", "manager"])

    def test_authorize_failure(self, user):
        assert not user.authorize(["admin"])