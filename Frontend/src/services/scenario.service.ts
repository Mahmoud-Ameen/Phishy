import api from "./api";
import { API_ENDPOINTS } from "../config/api";

export interface Template {
	id: number;
	scenario_id: number;
	subject: string | null;
	content: string | null;
}

export interface Scenario {
	id: number;
	name: string;
	description: string | null;
	level: number;
	template?: Template | null; 
}

export interface ScenarioData {
	name: string;
	description?: string | null;
	level: number;
}

interface ScenarioResponse {
	data: {
		scenario: Scenario; 
	};
	message: string;
	status: string;
}

// Response for GET all scenarios
interface ScenariosResponse {
	data: {
		scenarios: Scenario[]; 
	};
	message: string;
	status: string;
}

interface DeleteResponse {
	message: string;
	status: string;
}

export const scenarioService = {
	async getAll(): Promise<ScenariosResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.get<ScenariosResponse>(API_ENDPOINTS.scenarios, {
				headers,
			});
			return response.data;
		} catch (error) {
			console.error("Error fetching scenarios:", error);
			throw error;
		}
	},
	async getScenario(id: number): Promise<ScenarioResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.get<ScenarioResponse>(`${API_ENDPOINTS.scenarios}/${id}`, {
				headers,
			});
			return response.data;
		} catch (error) {
			console.error("Error fetching scenario:", error);
			throw error;
		}
	},

	async create(scenarioData: ScenarioData): Promise<ScenarioResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.post<ScenarioResponse>(
				API_ENDPOINTS.scenarios,
				scenarioData,
				{
					headers,
				}
			);
			return response.data;
		} catch (error) {
			console.error("Error creating scenario:", error);
			throw error;
		}
	},

	async update(id: number, scenarioData: ScenarioData): Promise<ScenarioResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.put<ScenarioResponse>(
				`${API_ENDPOINTS.scenarios}/${id}`,
				scenarioData,
				{ headers }
			);
			return response.data;
		} catch (error) {
			console.error("Error updating scenario:", error);
			throw error;
		}
	},

	async delete(id: number): Promise<DeleteResponse> {
		try {
			const token = localStorage.getItem("token");
			const headers = token ? { Authorization: `Bearer ${token}` } : {};
			const response = await api.delete(`${API_ENDPOINTS.scenarios}/${id}`, {
				headers,
			});
			return response.data;
		} catch (error) {
			console.error("Error deleting scenario:", error);
			throw error;
		}
	},
};
