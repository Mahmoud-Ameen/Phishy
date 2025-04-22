import requests
import json
from typing import Optional

BASE_URL = "http://localhost:3000/api"

class TestSeeder:
    def __init__(self):
        self.access_token: Optional[str] = None
        
    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}" if self.access_token else None
        }

    def register_admin(self):
        print("Registering admin user...")
        response = requests.post(
            f"{BASE_URL}/users",
            headers=self._headers(),
            json={
                "email": "admin@company.com",
                "password": "password",
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin"
            }
        )
        print(f"Register response: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.json()

    def login(self):
        print("\nLogging in...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            headers=self._headers(),
            json={
                "email": "admin@company.com",
                "password": "password"
            }
        )
        print(f"Login response: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        data = response.json()
        if data.get("status") == "success":
            self.access_token = data["data"]["access_token"]
        return data

    def create_departments(self):
        departments = ["IT", "HR", "Finance", "Marketing"]
        print("\nCreating departments...")
        
        results = []
        for dept in departments:
            response = requests.post(
                f"{BASE_URL}/departments",
                headers=self._headers(),
                json={"name": dept}
            )
            print(f"Create department {dept}: {response.status_code}")
            data = response.json()
            print(json.dumps(data, indent=2))
            if data.get("status") == "success":
                results.append(data["data"]["department"])
        return results

    def create_employees(self):
        employees = [
            {
                "email": "john@company.com",
                "first_name": "John",
                "last_name": "Doe",
                "criticality": "high",
                "dept_name": "IT"
            },
            {
                "email": "jane@company.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "criticality": "medium",
                "dept_name": "HR"
            },
            {
                "email": "bob@company.com",
                "first_name": "Bob",
                "last_name": "Johnson",
                "criticality": "low",
                "dept_name": "Finance"
            }
        ]
        
        print("\nCreating employees...")
        results = []
        for emp in employees:
            response = requests.post(
                f"{BASE_URL}/employees",
                headers=self._headers(),
                json=emp
            )
            print(f"Create employee {emp['email']}: {response.status_code}")
            data = response.json()
            print(json.dumps(data, indent=2))
            if data.get("status") == "success":
                results.append(data["data"]["employee"])
        return results

    def run(self):
        self.register_admin()
        self.login()
        self.create_departments()
        self.create_employees()


if __name__ == "__main__":
    seeder = TestSeeder()
    seeder.run()
