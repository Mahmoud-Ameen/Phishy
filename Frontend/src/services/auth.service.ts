import axios from "axios";
import { API_ENDPOINTS } from "../config/api";

interface LoginCredentials {
	email: string;
	password: string;
}

interface LoginResponse {
	data: {
		access_token: string;
	};
	message: string;
	status: string;
}

export const authService = {
	async login(credentials: LoginCredentials): Promise<LoginResponse> {
		try {
			const response = await axios.post<LoginResponse>(API_ENDPOINTS.login, credentials);

			const data = response.data;

			localStorage.setItem("token", data.data.access_token);
			return data;
		} catch (error) {
			console.error("Login failed:", error);
			throw new Error("Login failed");
		}
	},

	logout() {
		localStorage.removeItem("token");
	},

	isAuthenticated(): boolean {
		return !!localStorage.getItem("token");
	},
};
