import { useParams, useNavigate } from "react-router-dom";
import { scenarioService, Scenario } from "@/services/scenario.service";
import { templateService } from "@/services/template.service";
import resourceService, { Resource, CreateResourceData } from "@/services/resource.service";
import domainService, { Domain } from "@/services/domain.service";
import { useEffect, useState } from "react";
import DefaultLayout from "@/layouts/default";
import { Button } from "@heroui/button";
import { Input } from "@heroui/input";
import { Switch } from "@heroui/switch";
import { motion } from "framer-motion";
import { PencilIcon, TrashIcon, DocumentTextIcon, PlusIcon, ComputerDesktopIcon } from "@heroicons/react/24/outline";
import { toast } from 'react-toastify';

export default function ScenarioPage() {
	const { id } = useParams();
	const navigate = useNavigate();
	const [scenario, setScenario] = useState<Scenario>();
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [isEditing, setIsEditing] = useState(false);
	const [editedScenario, setEditedScenario] = useState<Partial<Scenario>>({});
	const [editedTemplate, setEditedTemplate] = useState<{
		subject: string;
		content: string;
	}>({
		subject: "",
		content: "",
	});

	// State for resources
	const [resources, setResources] = useState<Resource[]>([]);
	const [loadingResources, setLoadingResources] = useState<boolean>(true);
	const [resourceError, setResourceError] = useState<string | null>(null);

	// State for available domains
	const [availableDomains, setAvailableDomains] = useState<Domain[]>([]);
	const [loadingDomains, setLoadingDomains] = useState<boolean>(true);

	// State for adding a new resource
	const [showAddResourceForm, setShowAddResourceForm] = useState<boolean>(false);
	const [newResourceData, setNewResourceData] = useState<Omit<CreateResourceData, 'scenario_id'>>({
		domain_name: '',
		endpoint: '',
		content_type: 'text/html', // Default content type
		content: ''
	});
	const [isAddingResource, setIsAddingResource] = useState<boolean>(false);

	const fetchScenario = async () => {
		if (id) {
			try {
				setLoading(true);
				const response = await scenarioService.getScenario(Number(id));
				setScenario(response.data.scenario);
				if (response.data.scenario.template) {
					setEditedTemplate({
						subject: response.data.scenario.template.subject || "",
						content: response.data.scenario.template.content || "",
					});
				}
				setEditedScenario(response.data.scenario);
				setLoading(false);
			} catch (error) {
				console.error("Error fetching scenario:", error);
				setError("Failed to fetch scenario.");
				setLoading(false);
			}
		}
	};

	const fetchResources = async () => {
		if (id) {
			setLoadingResources(true);
			setResourceError(null);
			try {
				const fetchedResources = await resourceService.getResourcesByScenario(Number(id));
				setResources(fetchedResources);
			} catch (error) {
				console.error("Error fetching resources:", error);
				setResourceError("Failed to fetch resources for this scenario.");
			} finally {
				setLoadingResources(false);
			}
		}
	};

	const fetchDomains = async () => {
		setLoadingDomains(true);
		try {
			const fetchedDomains = await domainService.getDomains();
			setAvailableDomains(fetchedDomains);
			// Set default domain for new resource if domains exist
			if (fetchedDomains.length > 0) {
				 setNewResourceData(prev => ({ ...prev, domain_name: fetchedDomains[0].domain_name }));
			}
		} catch (error) {
			console.error("Error fetching domains:", error);
			toast.error('Failed to load available domains.');
		} finally {
			setLoadingDomains(false);
		}
	}

	useEffect(() => {
		fetchScenario();
		fetchResources(); // Fetch resources when component mounts or ID changes
		fetchDomains(); // Fetch domains for the add form
	}, [id]);

	const handleScenarioUpdate = async () => {
		if (!scenario?.id) return;

		try {
			await scenarioService.update(scenario.id, {
				name: editedScenario.name || "",
				description: editedScenario.description,
				level: editedScenario.level || 1,
			});

			if (scenario.template?.id) {
				await templateService.update(scenario.template.id, {
					subject: editedTemplate.subject,
					content: editedTemplate.content,
				});
			} else {
				await templateService.create({
					scenario_id: scenario.id,
					subject: editedTemplate.subject,
					content: editedTemplate.content,
				});
			}

			setIsEditing(false);
			await fetchScenario(); // Refresh data
		} catch (error) {
			console.error("Error updating scenario:", error);
			setError("Failed to update scenario.");
		}
	};

	const handleDelete = async () => {
		if (!scenario?.id || !window.confirm("Are you sure you want to delete this scenario?")) return;

		try {
			await scenarioService.delete(scenario.id);
			navigate("/scenarios");
		} catch (error) {
			console.error("Error deleting scenario:", error);
			setError("Failed to delete scenario.");
		}
	};

	// Handler for adding a resource
	const handleAddResource = async (e: React.FormEvent) => {
		e.preventDefault();
		if (!id || !newResourceData.domain_name || !newResourceData.endpoint.trim() || !newResourceData.content_type.trim() || !newResourceData.content.trim()) {
			toast.warn('Please fill in all resource fields.');
			return;
		}

		setIsAddingResource(true);
		try {
			const dataToCreate: CreateResourceData = {
				...newResourceData,
				scenario_id: Number(id),
				endpoint: newResourceData.endpoint.startsWith('/') ? newResourceData.endpoint : `/${newResourceData.endpoint}`, // Ensure leading slash
			};
			const createdResource = await resourceService.createResource(dataToCreate);
			setResources([...resources, createdResource]);
			toast.success('Resource added successfully!');
			// Reset form and hide
			setShowAddResourceForm(false);
			setNewResourceData({
				domain_name: availableDomains.length > 0 ? availableDomains[0].domain_name : '', // Reset domain
				endpoint: '',
				content_type: 'text/html',
				content: ''
			});

		} catch (error: any) {
			const errorMessage = error.response?.data?.message || 'Failed to add resource.';
			toast.error(errorMessage);
			console.error("Error adding resource:", error);
		} finally {
			setIsAddingResource(false);
		}
	};

	return (
		<DefaultLayout>
			<div className="max-w-4xl mx-auto p-6">
				{loading ? (
					<div className="flex items-center justify-center h-64">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500" />
					</div>
				) : error ? (
					<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
						<strong className="font-bold">Error! </strong>
						<span className="block sm:inline">{error}</span>
					</div>
				) : (
					<motion.div
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						className="space-y-8"
					>
						{/* Header */}
						<div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
							<div className="flex items-center gap-3">
								<DocumentTextIcon className="w-8 h-8 text-primary-500" />
								<h1 className="text-3xl font-bold text-gray-900">
									{isEditing ? "Edit Scenario" : scenario?.name}
								</h1>
							</div>
							<div className="flex items-center gap-4 self-end">
								<div className="flex items-center gap-2">
									<PencilIcon className="w-5 h-5 text-gray-500" />
									<button
										type="button"
										onClick={() => setIsEditing(!isEditing)}
										className={`${
											isEditing ? 'bg-primary-500' : 'bg-gray-200'
										} relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2`}
									>
										<span
											aria-hidden="true"
											className={`${
												isEditing ? 'translate-x-5' : 'translate-x-0'
											} pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
										/>
									</button>
									<span className="text-sm font-medium text-gray-700">
										{isEditing ? "Editing" : "View Mode"}
									</span>
								</div>
								{isEditing ? (
									<div className="flex gap-2">
										<Button
											color="primary"
											onClick={handleScenarioUpdate}
											className="flex items-center gap-2"
										>
											<span>Save Changes</span>
										</Button>
										<Button
											color="secondary"
											onClick={() => setIsEditing(false)}
											className="flex items-center gap-2"
										>
											<span>Cancel</span>
										</Button>
									</div>
								) : (
									<Button
										color="danger"
										onClick={handleDelete}
										className="flex items-center gap-2"
									>
										<TrashIcon className="w-5 h-5" />
										<span>Delete</span>
									</Button>
								)}
							</div>
						</div>

						{/* Scenario Details */}
						<div className="bg-white shadow-sm ring-1 ring-gray-900/5 rounded-lg p-6 space-y-6">
							<div className="flex items-center gap-2">
								<h2 className="text-xl font-semibold text-gray-900">Scenario Details</h2>
								{!isEditing && (
									<span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded-full">
										Level {scenario?.level}
									</span>
								)}
							</div>
							<div className="space-y-4">
								<div>
									<label className="block text-sm font-medium text-gray-700 mb-1">
										Name
									</label>
									<div className="min-h-[40px]">
										{isEditing ? (
											<Input
												value={editedScenario.name || ""}
												onChange={(e) =>
													setEditedScenario({
														...editedScenario,
														name: e.target.value,
													})
												}
												placeholder="Enter scenario name"
												className="w-full"
											/>
										) : (
											<p className="py-2 px-3 bg-gray-50 rounded-md">
												{scenario?.name}
											</p>
										)}
									</div>
								</div>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-1">
										Description
									</label>
									<div className="min-h-[96px]">
										{isEditing ? (
											<textarea
												value={editedScenario.description || ""}
												onChange={(e) =>
													setEditedScenario({
														...editedScenario,
														description: e.target.value,
													})
												}
												placeholder="Enter scenario description"
												className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
												rows={3}
											/>
										) : (
											<p className="py-2 px-3 bg-gray-50 rounded-md h-24 overflow-y-auto">
												{scenario?.description || "No description provided"}
											</p>
										)}
									</div>
								</div>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-1">
										Difficulty Level
									</label>
									<div className="min-h-[40px]">
										{isEditing ? (
											<div className="flex items-center gap-2">
												<Input
													type="number"
													min={1}
													max={5}
													value={String(editedScenario.level) || String(1)}
													onChange={(e) =>
														setEditedScenario({
															...editedScenario,
															level: parseInt(e.target.value),
														})
													}
													className="w-20"
												/>
												<span className="text-sm text-gray-500">(1-5)</span>
											</div>
										) : (
											<div className="py-2">
												<div className="flex items-center gap-2">
													<div className="flex gap-1">
														{[1, 2, 3, 4, 5].map((level) => (
															<div
																key={level}
																className={`w-6 h-2 rounded ${
																	level <= (scenario?.level || 0)
																		? "bg-primary-500"
																		: "bg-gray-200"
																}`}
															/>
														))}
													</div>
													<span className="text-sm text-gray-500">
														Level {scenario?.level}
													</span>
												</div>
											</div>
										)}
									</div>
								</div>
							</div>
						</div>

						{/* Template Section */}
						<div className="bg-white shadow-sm ring-1 ring-gray-900/5 rounded-lg p-6 space-y-6">
							<h2 className="text-xl font-semibold text-gray-900">Email Template</h2>
							<div className="space-y-4">
								<div>
									<label className="block text-sm font-medium text-gray-700 mb-1">
										Subject Line
									</label>
									<div className="min-h-[40px]">
										{isEditing ? (
											<Input
												value={editedTemplate.subject}
												onChange={(e) =>
													setEditedTemplate({
														...editedTemplate,
														subject: e.target.value,
													})
												}
												placeholder="Enter email subject"
												className="w-full"
											/>
										) : (
											<p className="py-2 px-3 bg-gray-50 rounded-md">
												{scenario?.template?.subject || "No subject"}
											</p>
										)}
									</div>
								</div>

								<div>
									<label className="block text-sm font-medium text-gray-700 mb-1">
										Email Content
									</label>
									<div className="min-h-[320px]">
										{isEditing ? (
											<textarea
												value={editedTemplate.content}
												onChange={(e) =>
													setEditedTemplate({
														...editedTemplate,
														content: e.target.value,
													})
												}
												placeholder="Enter email content"
												className="w-full h-[320px] rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 font-mono text-sm"
											/>
										) : (
											<div className="h-[320px] overflow-y-auto py-2 px-3 bg-gray-50 rounded-md">
												<pre className="whitespace-pre-wrap text-gray-900 font-mono text-sm">
													{scenario?.template?.content || "No content"}
												</pre>
											</div>
										)}
									</div>
								</div>
							</div>
						</div>

						{/* Resources Section */}
						<div className="bg-white shadow-sm ring-1 ring-gray-900/5 rounded-lg p-6 space-y-6">
							<div className="flex items-center justify-between">
								<div className="flex items-center gap-2">
									 <ComputerDesktopIcon className="w-6 h-6 text-primary-500" />
									 <h2 className="text-xl font-semibold text-gray-900">Phishing Resources (Landing Pages)</h2>
								</div>
								<Button 
									color="primary" 
									onClick={() => setShowAddResourceForm(!showAddResourceForm)}
									className="flex items-center gap-2"
									disabled={isAddingResource}
								>
									<PlusIcon className="w-5 h-5" />
									{showAddResourceForm ? 'Cancel' : 'Add Resource'}
								</Button>
							</div>

							{/* Add Resource Form (conditional) */}
							{showAddResourceForm && (
								<motion.form 
									initial={{ opacity: 0, height: 0 }} 
									animate={{ opacity: 1, height: 'auto' }} 
									exit={{ opacity: 0, height: 0 }}
									onSubmit={handleAddResource} 
									className="p-4 border rounded bg-gray-50 space-y-4"
								>
									 <h3 className="text-lg font-medium">New Resource Details</h3>
									 <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
										<div>
											<label htmlFor="resource-domain" className="block text-sm font-medium text-gray-700 mb-1">Domain</label>
											<select 
												id="resource-domain"
												value={newResourceData.domain_name}
												onChange={(e) => setNewResourceData({...newResourceData, domain_name: e.target.value})}
												className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
												disabled={loadingDomains || isAddingResource || availableDomains.length === 0}
											>
												{loadingDomains ? (
													<option>Loading domains...</option>
												) : availableDomains.length === 0 ? (
													<option>No domains available. Please add one first.</option>
												) : (
													availableDomains.map(domain => (
														<option key={domain.domain_name} value={domain.domain_name}>{domain.domain_name}</option>
													))
												)}
											</select>
										</div>
										<div>
											<label htmlFor="resource-endpoint" className="block text-sm font-medium text-gray-700 mb-1">Endpoint Path</label>
											<Input 
												id="resource-endpoint"
												type="text"
												placeholder="e.g., /login or /verify.html"
												value={newResourceData.endpoint}
												onChange={(e) => setNewResourceData({...newResourceData, endpoint: e.target.value})}
												className="w-full"
												disabled={isAddingResource}
											/>
										</div>
									 </div>
									<div>
										<label htmlFor="resource-content-type" className="block text-sm font-medium text-gray-700 mb-1">Content Type</label>
										<Input 
											id="resource-content-type"
											type="text"
											placeholder="e.g., text/html, application/json"
											value={newResourceData.content_type}
											onChange={(e) => setNewResourceData({...newResourceData, content_type: e.target.value})}
											className="w-full"
											disabled={isAddingResource}
										/>
									</div>
									 <div>
										 <label htmlFor="resource-content" className="block text-sm font-medium text-gray-700 mb-1">Content (HTML, JSON, etc.)</label>
										 <textarea
											 id="resource-content"
											 rows={8}
											 value={newResourceData.content}
											 onChange={(e) => setNewResourceData({...newResourceData, content: e.target.value})}
											 className="w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 font-mono text-sm"
											 placeholder="Paste your HTML code or other content here..."
											 disabled={isAddingResource}
										 />
									 </div>
									 <div className="flex justify-end">
										 <Button 
											type="submit" 
											color="primary" 
											disabled={isAddingResource || availableDomains.length === 0}
											className="flex items-center gap-2"
										>
											 {isAddingResource ? 'Adding...' : 'Save Resource'}
										 </Button>
									 </div>
								</motion.form>
							)}

							{/* Resources List Table */}
							<div className="overflow-x-auto">
								{loadingResources ? (
									<p className="text-center text-gray-500 py-4">Loading resources...</p>
								) : resourceError ? (
									 <p className="text-center text-red-600 py-4">{resourceError}</p>
								) : (
									<table className="min-w-full divide-y divide-gray-200">
										<thead className="bg-gray-50">
											<tr>
												<th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Domain</th>
												<th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Endpoint</th>
												<th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Content Type</th>
												<th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Created</th>
												{/* Add Actions column if needed later */}
												<th scope="col" className="relative px-6 py-3">
													<span className="sr-only">Actions</span>
												</th>
											</tr>
										</thead>
										<tbody className="bg-white divide-y divide-gray-200">
											{resources.length === 0 ? (
												<tr>
													<td colSpan={5} className="px-6 py-4 text-center text-gray-500">No resources found for this scenario.</td>
												</tr>
											) : (
												resources.map((resource) => (
													<tr key={resource.id}>
														<td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{resource.domain_name}</td>
														<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700 font-mono">{resource.endpoint}</td>
														<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{resource.content_type}</td>
														<td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
															{resource.created_at ? new Date(resource.created_at).toLocaleString() : 'N/A'}
														</td>
														<td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
															{/* Add Edit/Delete buttons here later */}
															<Button variant="light" color="secondary" size="sm">View</Button> 
														</td>
													</tr>
												))
											)}
										</tbody>
									</table>
								)}
							</div>
						</div>
					</motion.div>
				)}
			</div>
		</DefaultLayout>
	);
}
