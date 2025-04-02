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
			const response = await fetch(API_ENDPOINTS.login, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(credentials),
			});

			if (!response.ok) {
				throw new Error("Login failed");
			}

			const data = await response.json();
			// Store the token in localStorage
			localStorage.setItem("token", data.data.access_token);
			return data;
		} catch (error) {
			throw error;
		}
	},

	logout() {
		localStorage.removeItem("token");
	},

	isAuthenticated(): boolean {
		return !!localStorage.getItem("token");
	},
};
