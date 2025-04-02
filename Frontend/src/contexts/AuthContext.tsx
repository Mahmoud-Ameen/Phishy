import React, { createContext, useContext, useState, useEffect } from "react";
import { authService } from "../services/auth.service";
import { jwtDecode } from "jwt-decode";

interface User {
	id: string;
	email: string;
	name: string;
	role: string;
}

interface JwtPayload {
	sub: string;
	email: string;
	name: string;
	role: string;
	iat: number;
	exp: number;
}

interface AuthContextType {
	user: User | null;
	isAuthenticated: boolean;
	isLoading: boolean;
	login: (email: string, password: string) => Promise<void>;
	logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const isTokenExpired = (token: string): boolean => {
	try {
		const decoded = jwtDecode<JwtPayload>(token);
		const currentTime = Date.now() / 1000;
		return decoded.exp < currentTime;
	} catch (error) {
		console.error("Error decoding token for expiration check:", error);
		return true; // If there's an error decoding, consider it expired
	}
};

const extractUserFromToken = (token: string): User | null => {
	try {
		// Check if token is expired before extracting user data
		if (isTokenExpired(token)) {
			return null;
		}

		const decoded = jwtDecode<JwtPayload>(token);
		return {
			id: decoded.sub,
			email: decoded.email,
			name: decoded.name,
			role: decoded.role,
		};
	} catch (error) {
		console.error("Error decoding token:", error);
		return null;
	}
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
	const [user, setUser] = useState<User | null>(null);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		// Check if user is already logged in on mount
		const checkAuth = async () => {
			try {
				const token = localStorage.getItem("token");
				if (token) {
					// Verify token isn't expired
					if (isTokenExpired(token)) {
						// Token is expired, remove it
						localStorage.removeItem("token");
					} else {
						const userData = extractUserFromToken(token);
						if (userData) {
							setUser(userData);
							console.log("Logged In. User data:", userData);
						} else {
							// If token is invalid, remove it
							localStorage.removeItem("token");
						}
					}
				}
			} catch (error) {
				console.error("Auth check failed:", error);
			} finally {
				setIsLoading(false);
			}
		};

		checkAuth();
	}, []);

	const login = async (email: string, password: string) => {
		try {
			const response = await authService.login({ email, password });
			const userData = extractUserFromToken(response.data.access_token);
			if (userData) {
				setUser(userData);
				console.log("Logged In. User data:", userData);
			} else {
				throw new Error("Invalid token received");
			}
		} catch (error) {
			throw error;
		}
	};

	const logout = () => {
		authService.logout();
		setUser(null);
	};

	return (
		<AuthContext.Provider
			value={{
				user,
				isAuthenticated: !!user,
				isLoading,
				login,
				logout,
			}}>
			{children}
		</AuthContext.Provider>
	);
};

export const useAuth = () => {
	const context = useContext(AuthContext);
	if (context === undefined) {
		throw new Error("useAuth must be used within an AuthProvider");
	}
	return context;
};
