import axios from "axios";
import { API_ENDPOINTS } from "../config/api";

interface Scenario {
	id: number;
	name: string;
	description: string | null;
	level: number;
}

interface Template {
	id: number;
	scenario_id: number;
	subject: string | null;
	content: string | null;
}

interface TemplateData {
	scenario_id: number;
	subject?: string | null;
	content?: string | null;
}

interface TemplateResponse {
	data: {
		template: Template;
	};
	message: string;
	status: string;
}

interface TemplatesResponse {
	data: {
		templates: Template[];
	};
	message: string;
	status: string;
}

export const templateService = {
	async getAll(): Promise<TemplatesResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.get(API_ENDPOINTS.templates, { headers });
			return response.data;
		} catch (error) {
			console.error("Error fetching templates:", error);
			throw error;
		}
	},

	async create(templateData: TemplateData): Promise<TemplateResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.post(API_ENDPOINTS.templates, templateData, {
				headers,
			});
			return response.data;
		} catch (error) {
			console.error("Error creating template:", error);
			throw error;
		}
	},

	async update(
		id: number,
		templateData: Partial<Omit<Template, "id" | "scenario_id">>
	): Promise<TemplateResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.put(`${API_ENDPOINTS.templates}/${id}`, templateData, {
				headers,
			});
			return response.data;
		} catch (error) {
			console.error("Error updating template:", error);
			throw error; 
		}
	},

	async delete(id: number): Promise<{ message: string; status: string }> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await axios.delete(`${API_ENDPOINTS.templates}/${id}`, { headers });
			return response.data;
		} catch (error) {
			console.error("Error deleting template:", error);
			throw error; 
		}
	},
};
