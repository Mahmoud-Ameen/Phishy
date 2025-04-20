import axios from "axios";
import { API_ENDPOINTS } from "../config/api";

enum Criticality {
	LOW = "low",
	MEDIUM = "medium",
	HIGH = "high",
}

interface Employee {
	email: string;
	first_name: string;
	last_name: string;
	criticality: Criticality;
	dept_name: string;
}

interface EmployeeData {
	email: string;
	first_name: string;
	last_name: string;
	criticality: Criticality;
	dept_name: string;
}

interface EmployeesResponse {
	data: {
		employees: Employee[];
	};
	message: string;
	status: string;
}

interface CreateEmployeeResponse {
	data: {
		employee: Employee;
	};
	message: string;
	status: string;
}

export const employeeService = {
	async getAll(): Promise<EmployeesResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.get(API_ENDPOINTS.employees, { headers });
			return response.data;
		} catch (error) {
			console.error("Error fetching employees:", error);
			throw error;
		}
	},

	async create(employeeData: EmployeeData): Promise<CreateEmployeeResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.post(API_ENDPOINTS.employees,  employeeData, {headers});
			return response.data;
		} catch (error) {
			console.error("Error creating employee:", error);
			if (axios.isAxiosError(error) && error.response?.status === 409) {
				throw new Error("Employee already exists");
			}
			throw error;
		}
	},
};
