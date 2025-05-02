import api from "./api";
import { API_ENDPOINTS } from "../config/api";

interface Department {
	name: string;
}

interface DepartmentsResponse {
	data: {
		departments: Department[];
	};
	message: string;
	status: string;
}

interface CreateDepartmentResponse {
	data: {
		department: Department;
	};
	message: string;
	status: string;
}

export const departmentService = {
	async getAll(): Promise<DepartmentsResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.get<DepartmentsResponse>(API_ENDPOINTS.departments, { headers });
			return response.data;
		} catch (error) {
			console.error("Error fetching departments:", error);
			throw error;
		}
	},

	async create(name: string): Promise<CreateDepartmentResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.post(API_ENDPOINTS.departments, { name }, { headers });
			return response.data;
		} catch (error) {
			console.error("Error creating department:", error);
			throw error;
		}
	},
};
