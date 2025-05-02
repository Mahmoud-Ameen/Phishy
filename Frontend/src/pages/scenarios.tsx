import { useState, useEffect, useMemo, useCallback } from "react";
import DefaultLayout from "@/layouts/default";
import {
	Table,
	TableHeader,
	TableColumn,
	TableBody,
	TableRow,
	TableCell,
	Button,
	Modal,
	ModalContent,
	ModalHeader,
	ModalBody,
	ModalFooter,
	Input,
	Textarea,
	useDisclosure,
	Spinner,
} from "@heroui/react";
import { PlusIcon } from "@heroicons/react/24/outline";
import { useAuth } from "../contexts/AuthContext";
import { scenarioService } from "../services/scenario.service";
import { templateService } from "../services/template.service";
import { useNavigate } from "react-router-dom";

interface Scenario {
	id: number;
	name: string;
	description: string | null;
	level: number;
	template?: Template | null;
}

interface Template {
	id: number;
	scenario_id: number;
	subject: string | null;
	content: string | null;
}

export default function ScenariosPage() {
	// Modal controls
	const {
		isOpen: isScenarioModalOpen,
		onOpen: onScenarioModalOpen,
		onClose: onScenarioModalClose,
	} = useDisclosure();
	const {
		isOpen: isTemplateModalOpen,
		onOpen: onTemplateModalOpen,
		onClose: onTemplateModalClose,
	} = useDisclosure();
	const {
		isOpen: isPreviewModalOpen,
		onOpen: onPreviewModalOpen,
		onClose: onPreviewModalClose,
	} = useDisclosure();

	const { user } = useAuth();
	const navigate = useNavigate();

	// State
	const [scenarios, setScenarios] = useState<Scenario[]>([]);
	const [editingScenario, setEditingScenario] = useState<Scenario | null>(null);
	const [newScenario, setNewScenario] = useState<Partial<Scenario>>({});

	const [editingTemplate, setEditingTemplate] = useState<Template | null>(null);
	const [templateScenarioId, setTemplateScenarioId] = useState<number | null>(null);
	const [newOrEditingTemplateData, setNewOrEditingTemplateData] = useState<
		Partial<Omit<Template, "id" | "scenario_id">>
	>({});
	const [previewContent, setPreviewContent] = useState<string | null>(null);

	const [scenarioError, setScenarioError] = useState<string | null>(null);
	const [templateError, setTemplateError] = useState<string | null>(null);
	const [loading, setLoading] = useState<boolean>(true);

	// Load scenarios on component mount
	useEffect(() => {
		fetchScenarios();
	}, []);

	// Sort scenarios by level
	const sortedScenarios = useMemo(() => {
		return [...scenarios].sort((a, b) => a.level - b.level);
	}, [scenarios]);

	const fetchScenarios = async () => {
		setLoading(true);
		try {
			setScenarioError(null);
			const response = await scenarioService.getAll();
			setScenarios(response.data.scenarios);
		} catch (error) {
			console.error("Error fetching scenarios:", error);
			setScenarioError("Failed to load scenarios.");
		} finally {
			setLoading(false);
		}
	};

	const handleCreateScenario = async () => {
		setScenarioError(null);
		if (!newScenario.name || !newScenario.level) {
			setScenarioError("Scenario Name and Level are required.");
			return;
		}
		try {
			const response = await scenarioService.create({
				name: newScenario.name,
				description: newScenario.description,
				level: newScenario.level,
			});
			setScenarios([...scenarios, { ...response.data.scenario, template: null }]);
			setNewScenario({});
			onScenarioModalClose();
		} catch (error: any) {
			console.error("Error creating scenario:", error);
			setScenarioError(error.response?.data?.message || "Failed to create scenario.");
		}
	};

	const handleEditScenario = async () => {
		setScenarioError(null);
		if (!editingScenario) return;
		try {
			const response = await scenarioService.update(editingScenario.id, {
				name: editingScenario.name,
				description: editingScenario.description,
				level: editingScenario.level,
			});
			setScenarios(
				scenarios.map((s) =>
					s.id === response.data.scenario.id ? 
					  { ...response.data.scenario, template: s.template } : s
				)
			);
			setEditingScenario(null);
			onScenarioModalClose();
		} catch (error: any) {
			console.error("Error updating scenario:", error);
			setScenarioError(error.response?.data?.message || "Failed to update scenario.");
		}
	};

	const handleDeleteScenario = async (id: number) => {
		setScenarioError(null);
		try {
			await scenarioService.delete(id);
			setScenarios(scenarios.filter((s) => s.id !== id));
		} catch (error: any) {
			console.error("Error deleting scenario:", error);
			setScenarioError(error.response?.data?.message || "Failed to delete scenario.");
		}
	};

	const handleSaveTemplate = async () => {
		setTemplateError(null);
		if (!newOrEditingTemplateData.subject || !newOrEditingTemplateData.content) {
			setTemplateError("Subject and Content cannot be empty.");
			return;
		}
		try {
			let savedTemplate: Template;
			if (editingTemplate) {
				const response = await templateService.update(editingTemplate.id, {
					subject: newOrEditingTemplateData.subject,
					content: newOrEditingTemplateData.content,
				});
				savedTemplate = response.data.template;
				setEditingTemplate(null);
			} else if (templateScenarioId) {
				const response = await templateService.create({
					scenario_id: templateScenarioId,
					subject: newOrEditingTemplateData.subject,
					content: newOrEditingTemplateData.content,
				});
				savedTemplate = response.data.template;
				setTemplateScenarioId(null);
			} else {
				throw new Error("Cannot save template without scenario context.");
			}
			setScenarios(
				scenarios.map((s) =>
					s.id === savedTemplate.scenario_id ? { ...s, template: savedTemplate } : s
				)
			);
			setNewOrEditingTemplateData({});
			onTemplateModalClose();
		} catch (error: any) {
			console.error("Error saving template:", error);
			setTemplateError(error.response?.data?.message || "Failed to save template.");
		}
	};

	const handleDeleteTemplate = async (templateId: number, scenarioId: number) => {
		setTemplateError(null);
		try {
			await templateService.delete(templateId);
			setScenarios(
				scenarios.map((s) => (s.id === scenarioId ? { ...s, template: null } : s))
			);
		} catch (error: any) {
			console.error("Error deleting template:", error);
			setTemplateError(error.response?.data?.message || "Failed to delete template.");
		}
	};

	// Memoized handlers for opening modals
	const openScenarioModalForEdit = useCallback((scenario: Scenario) => {
		setEditingScenario({ ...scenario });
		setNewScenario({});
		onScenarioModalOpen();
	}, [onScenarioModalOpen]);

	const openScenarioModalForCreate = useCallback(() => {
		setEditingScenario(null);
		setNewScenario({});
		onScenarioModalOpen();
	}, [onScenarioModalOpen]);

	const openTemplateModalForCreate = useCallback((scenarioId: number) => {
		setEditingTemplate(null);
		setTemplateScenarioId(scenarioId);
		setNewOrEditingTemplateData({});
		setTemplateError(null);
		onTemplateModalOpen();
	}, [onTemplateModalOpen]);

	const openTemplateModalForEdit = useCallback((template: Template) => {
		setEditingTemplate(template);
		setTemplateScenarioId(null);
		setNewOrEditingTemplateData({
			subject: template.subject,
			content: template.content,
		});
		setTemplateError(null);
		onTemplateModalOpen();
	}, [onTemplateModalOpen]);

	const openPreviewModal = useCallback((content: string | null) => {
		setPreviewContent(content);
		onPreviewModalOpen();
	}, [onPreviewModalOpen]);

	if (loading) {
		return (
			<DefaultLayout>
				<div className="flex justify-center items-center h-[calc(100vh-4rem)]">
					<Spinner size="lg" />
				</div>
			</DefaultLayout>
		);
	}

	return (
		<DefaultLayout>
			<div className="px-6 py-4 space-y-6">
				<div>
					<div className="flex justify-between items-center mb-4">
						<h1 className="text-3xl font-semibold text-[#0077B6]">
							Scenarios & Templates
						</h1>
						<Button
							color="primary"
							endContent={<PlusIcon className="h-5 w-5" />}
							onPress={openScenarioModalForCreate}>
							Create Scenario
						</Button>
					</div>

					{scenarioError && (
						<p className="text-red-500 mb-4">
							Error loading scenarios: {scenarioError}
						</p>
					)}
					{templateError && (
						<p className="text-red-500 mb-4">
							Error loading templates: {templateError}
						</p>
					)}

					{scenarios.length === 0 ? (
						<div className="text-center p-8 bg-default-100 rounded-lg">
							<p className="text-default-600 mb-4">No scenarios found.</p>
							<Button color="primary" onPress={openScenarioModalForCreate}>
								Create Your First Scenario
							</Button>
						</div>
					) : (
						<Table aria-label="Scenarios and Templates List">
							<TableHeader>
								<TableColumn key="scenarioName">SCENARIO</TableColumn>
								<TableColumn key="scenarioLevel">LEVEL</TableColumn>
								<TableColumn key="templateSubject">TEMPLATE SUBJECT</TableColumn>
							</TableHeader>
							<TableBody items={sortedScenarios} emptyContent="No scenarios found.">
								{(item) => {
									const { template } = item;
									const scenario = item;

									return (
										<TableRow
											key={scenario.id}
											onClick={() => {
												navigate(`/scenario/${scenario.id}`);
											}}
											className="cursor-pointer hover:bg-gray-100">
											<TableCell>{scenario.name}</TableCell>
											<TableCell>Level {scenario.level}</TableCell>
											<TableCell>{template?.subject || "-"}</TableCell>
										</TableRow>
									);
								}}
							</TableBody>
						</Table>
					)}
				</div>

				<Modal
					isOpen={isScenarioModalOpen}
					onClose={onScenarioModalClose}
					isDismissable={false}
					hideCloseButton={true}>
					<ModalContent>
						<ModalHeader>
							{editingScenario ? "Edit Scenario" : "Create New Scenario"}
						</ModalHeader>
						<ModalBody>
							{scenarioError && (
								<p className="text-red-500 text-sm mb-2">{scenarioError}</p>
							)}
							<div className="space-y-4">
								<Input
									label="Scenario Name"
									placeholder="Enter scenario name"
									value={editingScenario?.name || newScenario.name || ""}
									onValueChange={(value) =>
										editingScenario
											? setEditingScenario({
													...editingScenario,
													name: value,
												})
											: setNewScenario({ ...newScenario, name: value })
									}
									isRequired
								/>
								<Textarea
									label="Description"
									placeholder="Enter scenario description"
									value={
										editingScenario?.description ||
										newScenario.description ||
										""
									}
									onValueChange={(value) =>
										editingScenario
											? setEditingScenario({
													...editingScenario,
													description: value,
												})
											: setNewScenario({ ...newScenario, description: value })
									}
								/>
								<Input
									type="number"
									label="Level"
									placeholder="Enter difficulty level (1-5)"
									min={1}
									max={5}
									value={String(
										editingScenario?.level || newScenario.level || ""
									)}
									onValueChange={(value) => {
										const level = parseInt(value) || 0;
										if (editingScenario) {
											setEditingScenario({ ...editingScenario, level });
										} else {
											setNewScenario({ ...newScenario, level });
										}
									}}
									isRequired
								/>
							</div>
						</ModalBody>
						<ModalFooter>
							<Button color="danger" variant="light" onPress={onScenarioModalClose}>
								Cancel
							</Button>
							<Button
								color="primary"
								onPress={
									editingScenario ? handleEditScenario : handleCreateScenario
								}
								isDisabled={
									!(editingScenario?.name || newScenario.name) ||
									!(editingScenario?.level || newScenario.level)
								}>
								{editingScenario ? "Update" : "Create"} Scenario
							</Button>
						</ModalFooter>
					</ModalContent>
				</Modal>

				<Modal
					isOpen={isTemplateModalOpen}
					onClose={onTemplateModalClose}
					isDismissable={false}
					hideCloseButton={true}>
					<ModalContent>
						<ModalHeader>
							{editingTemplate
								? `Edit Template for ${scenarios.find((s) => s.id === editingTemplate.scenario_id)?.name || "Unknown"}`
								: `Create New Template for ${scenarios.find((s) => s.id === templateScenarioId)?.name || "Unknown"}`}
						</ModalHeader>
						<ModalBody>
							{templateError && (
								<p className="text-red-500 text-sm mb-2">{templateError}</p>
							)}
							<p className="text-sm text-gray-600 mb-4">
								Scenario ID:{" "}
								{editingTemplate ? editingTemplate.scenario_id : templateScenarioId}
							</p>
							<div className="space-y-4">
								<Input
									label="Subject"
									placeholder="Enter email subject"
									value={newOrEditingTemplateData.subject || ""}
									onValueChange={(value) =>
										setNewOrEditingTemplateData({
											...newOrEditingTemplateData,
											subject: value,
										})
									}
									isRequired
								/>
								<Textarea
									label="Content"
									placeholder="Enter email content (HTML allowed)"
									value={newOrEditingTemplateData.content || ""}
									onValueChange={(value) =>
										setNewOrEditingTemplateData({
											...newOrEditingTemplateData,
											content: value,
										})
									}
									minRows={5}
									isRequired
								/>
							</div>
						</ModalBody>
						<ModalFooter>
							<Button color="danger" variant="light" onPress={onTemplateModalClose}>
								Cancel
							</Button>
							<Button color="primary" onPress={handleSaveTemplate}>
								{editingTemplate ? "Update" : "Create"} Template
							</Button>
						</ModalFooter>
					</ModalContent>
				</Modal>

				<Modal size="3xl" isOpen={isPreviewModalOpen} onClose={onPreviewModalClose}>
					<ModalContent>
						<ModalHeader>Template Preview</ModalHeader>
						<ModalBody>
							{previewContent ? (
								<div
									className="max-w-none border p-4 rounded bg-white h-96 overflow-auto"
									dangerouslySetInnerHTML={{ __html: previewContent }}
								/>
							) : (
								<p>No content to preview.</p>
							)}
						</ModalBody>
						<ModalFooter>
							<Button color="primary" onPress={onPreviewModalClose}>
								Close
							</Button>
						</ModalFooter>
					</ModalContent>
				</Modal>
			</div>
		</DefaultLayout>
	);
}
