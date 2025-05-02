// TODO: Use env variables
export const API_BASE_URL = "https://exact-hound-rationally.ngrok-free.app/api";

export const API_ENDPOINTS = {
	login: `${API_BASE_URL}/auth/login`,
	scenarios: `${API_BASE_URL}/scenarios`,
	templates: `${API_BASE_URL}/templates`,
	employees: `${API_BASE_URL}/employees`,
	departments: `${API_BASE_URL}/departments`,
	campaigns: `${API_BASE_URL}/campaigns`,
	domains: `${API_BASE_URL}/domains`,
	resources: `${API_BASE_URL}/resources`,
};
