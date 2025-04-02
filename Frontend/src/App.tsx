// External
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";

// App imports
import LoginPage from "@/pages/login";
import OverviewPage from "@/pages/overview";
import CampaignsPage from "@/pages/campaigns";
import BlogPage from "@/pages/blog";
import AboutPage from "@/pages/about";

function App() {
	return (
		<AuthProvider>
			<Routes>
				{/* Public routes */}
				<Route path="/login" element={<LoginPage />} />
				<Route path="/about" element={<AboutPage />} />
				<Route path="/blog" element={<BlogPage />} />

				{/* Protected routes */}
				<Route
					path="/overview"
					element={
						<ProtectedRoute>
							<OverviewPage />
						</ProtectedRoute>
					}
				/>
				<Route
					path="/campaigns"
					element={
						<ProtectedRoute>
							<CampaignsPage />
						</ProtectedRoute>
					}
				/>

				{/* Redirect root to overview */}
				<Route path="/" element={<Navigate to="/overview" replace />} />
			</Routes>
		</AuthProvider>
	);
}

export default App;
