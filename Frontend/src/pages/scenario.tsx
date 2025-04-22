import { useParams, useNavigate } from "react-router-dom";
import { scenarioService, Scenario } from "@/services/scenario.service";
import { templateService } from "@/services/template.service";
import { useEffect, useState } from "react";
import DefaultLayout from "@/layouts/default";
import { Button } from "@heroui/button";
import { Input } from "@heroui/input";
import { Switch } from "@heroui/switch";
import { motion } from "framer-motion";
import { PencilIcon, TrashIcon, DocumentTextIcon } from "@heroicons/react/24/outline";

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

	useEffect(() => {
		fetchScenario();
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
					</motion.div>
				)}
			</div>
		</DefaultLayout>
	);
}
