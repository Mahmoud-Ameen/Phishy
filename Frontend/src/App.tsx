// External
import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";

// App imports
import LoginPage from "@/pages/login";
import OverviewPage from "@/pages/overview";
import CampaignsPage from "@/pages/campaigns";
import ScenariosPage from "@/pages/scenarios";
import EmployeesPage from "@/pages/employees";
import BlogPage from "@/pages/blog";
import AboutPage from "@/pages/about";
import ScnearioPage from "@/pages/scenario";
import CreateCampaignPage from "./pages/campaigns/create";
import CampaignDetailsPage from "./pages/campaigns/details";
import DomainsPage from "./pages/Admin/DomainsPage";

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
				<Route
					path="/campaigns/create"
					element={
						<ProtectedRoute>
								<CreateCampaignPage/>
						</ProtectedRoute>
					} 
				/>
				<Route
					path="/campaigns/:id"
					element={
						<ProtectedRoute>
								<CampaignDetailsPage/>
						</ProtectedRoute>
					} 
				/>
				<Route
					path="/scenarios"
					element={
						<ProtectedRoute>
							<ScenariosPage />
						</ProtectedRoute>
					}
				/>
				<Route
					path="/scenario/:id"
					element={
						<ProtectedRoute>
							<ScnearioPage />
						</ProtectedRoute>
					}
				/>

				<Route
					path="/employees"
					element={
						<ProtectedRoute>
							<EmployeesPage />
						</ProtectedRoute>
					}
				/>

				{/* Domain Management Route */}
				<Route
					path="/admin/domains"
					element={
						<ProtectedRoute>
							<DomainsPage />
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
