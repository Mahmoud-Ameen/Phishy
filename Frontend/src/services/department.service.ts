import axios from "axios";
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
			const response = await axios.get<{
				data: { departments: string[] };
				message: string;
				status: string;
			}>(API_ENDPOINTS.departments, { headers });
			const departmentsArray = response.data.data.departments.map((name) => ({
				name,
			}));
			const result: DepartmentsResponse = {
				message: response.data.message,
				status: response.data.status,
				data: {
					departments: departmentsArray,
				},
			};
			return result;
		} catch (error) {
			console.error("Error fetching departments:", error);
			throw error;
		}
	},

	async create(name: string): Promise<CreateDepartmentResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.post(API_ENDPOINTS.departments, { name }, { headers });
			return response.data;
		} catch (error) {
			console.error("Error creating department:", error);
			throw error;
		}
	},
};
