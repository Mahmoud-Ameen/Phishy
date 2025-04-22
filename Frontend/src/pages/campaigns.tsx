import { useEffect, useState } from "react";
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
	Select,
	SelectItem,
	useDisclosure,
	Selection,
	Chip,
	Spinner,
	Progress,
	CheckboxGroup,
	Checkbox,
} from "@heroui/react";
import { PlusIcon, ChartBarIcon } from "@heroicons/react/24/outline";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Campaign, CampaignStatus, campaignService } from "@/services/campaign.service";
import { Scenario, scenarioService } from "@/services/scenario.service";
import { employeeService } from "@/services/employee.service";
import { toast } from "react-hot-toast";

interface CampaignWithStatus extends Campaign {
	scenario?: Scenario;
	status?: CampaignStatus;
}

interface Employee {
	email: string;
	first_name: string;
	last_name: string;
	criticality: string;
	dept_name: string;
}

export default function CampaignPage() {
	const navigate = useNavigate();
	const { isOpen: isStatsOpen, onOpen: onStatsOpen, onClose: onStatsClose } = useDisclosure();
	const [campaigns, setCampaigns] = useState<CampaignWithStatus[]>([]);
	const [scenarios, setScenarios] = useState<Scenario[]>([]);
	const [employees, setEmployees] = useState<Employee[]>([]);
	const [loading, setLoading] = useState(true);
	const [selectedCampaign, setSelectedCampaign] = useState<CampaignWithStatus | null>(null);

	useEffect(() => {
		fetchCampaigns();
		fetchScenarios();
		fetchEmployees();
	}, []);

	const fetchCampaigns = async () => {
		try {
			const response = await campaignService.getCampaigns();
			const campaignsWithStatus = await Promise.all(
				response.data.campaigns.map(async (campaign) => {
					try {
						const statusResponse = await campaignService.getCampaignStatus(campaign.id);
						const scenarioResponse = await scenarioService.getScenario(campaign.scenario_id);
						return { 
							...campaign, 
							status: statusResponse.data.status,
							scenario: scenarioResponse.data.scenario
						};
					} catch (error) {
						console.error(`Error fetching details for campaign ${campaign.id}:`, error);
						return campaign;
					}
				})
			);
			setCampaigns(campaignsWithStatus);
		} catch (error) {
			console.error("Error fetching campaigns:", error);
			toast.error("Failed to load campaigns");
		} finally {
			setLoading(false);
		}
	};

	const fetchScenarios = async () => {
		try {
			const response = await scenarioService.getAll();
			setScenarios(response.data.scenarios);
		} catch (error) {
			console.error("Error fetching scenarios:", error);
			toast.error("Failed to load scenarios");
		}
	};

	const fetchEmployees = async () => {
		try {
			const response = await employeeService.getAll();
			setEmployees(response.data.employees);
		} catch (error) {
			console.error("Error fetching employees:", error);
			toast.error("Failed to load employees");
		}
	};
	const handleViewStats = async (campaign: CampaignWithStatus) => {
		setSelectedCampaign(campaign);
		onStatsOpen();
	};

	const formatDate = (dateString: string) => {
		return new Date(dateString).toLocaleDateString();
	};

	const getProgressColor = (percentage: number) => {
		if (percentage < 30) return "danger";
		if (percentage < 70) return "warning";
		return "success";
	};

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
			<div className="px-6 py-4">
				<div className="flex justify-between items-center mb-6">
					<h1 className="text-3xl font-semibold text-[#0077B6]">Campaigns</h1>
					<Button
						color="primary"
						endContent={<PlusIcon className="h-5 w-5" />}
						onPress={() => navigate("/campaigns/create")}>
						Create Campaign
					</Button>
				</div>

				<Table aria-label="Phishing campaigns">
					<TableHeader>
						<TableColumn>NAME</TableColumn>
						<TableColumn>SCENARIO</TableColumn>
						<TableColumn>START DATE</TableColumn>
						<TableColumn>PROGRESS</TableColumn>
						<TableColumn>ACTIONS</TableColumn>
					</TableHeader>
					<TableBody>
						{campaigns.map((campaign) => (
							<TableRow key={campaign.id}>
								<TableCell>{campaign.name}</TableCell>
								<TableCell>
									{campaign.scenario?.name || `Scenario ${campaign.scenario_id}`}
									{campaign.scenario?.level && (
										<Chip
											size="sm"
											color={campaign.scenario.level > 2 ? "danger" : "warning"}
											className="ml-2">
											Level {campaign.scenario.level}
										</Chip>
									)}
								</TableCell>
								<TableCell>{formatDate(campaign.start_date)}</TableCell>
								<TableCell>
									{campaign.status ? (
										<div className="w-full max-w-md">
											<div className="flex justify-between text-small mb-1">
												<span>Sent: {campaign.status.sent_emails}/{campaign.status.total_emails}</span>
												<span className="text-foreground/50">{Math.round((campaign.status.sent_emails / campaign.status.total_emails) * 100)}%</span>
											</div>
											<Progress
												aria-label="Campaign progress"
												value={(campaign.status.sent_emails / campaign.status.total_emails) * 100}
												color={getProgressColor((campaign.status.sent_emails / campaign.status.total_emails) * 100)}
												className="w-full"
											/>
										</div>
									) : (
										"Loading..."
									)}
								</TableCell>
								<TableCell>
									<Button
										color="secondary"
										variant="light"
										size="sm"
										startContent={<ChartBarIcon className="h-4 w-4" />}
										onPress={() => handleViewStats(campaign)}>
										View Stats
									</Button>
								</TableCell>
							</TableRow>
						))}
					</TableBody>
				</Table>

				{/* Campaign Stats Modal */}
				<Modal isOpen={isStatsOpen} onClose={onStatsClose}>
					<ModalContent>
						<ModalHeader>Campaign Statistics</ModalHeader>
						<ModalBody>
							{selectedCampaign?.status ? (
								<div className="space-y-4">
									<h3 className="text-xl font-semibold">{selectedCampaign.name}</h3>
									<div className="grid grid-cols-2 gap-4">
										<div className="p-4 rounded-lg bg-default-100">
											<div className="text-2xl font-bold">{selectedCampaign.status.sent_emails}</div>
											<div className="text-sm text-default-600">Emails Sent</div>
										</div>
										<div className="p-4 rounded-lg bg-default-100">
											<div className="text-2xl font-bold">{selectedCampaign.status.opened_emails}</div>
											<div className="text-sm text-default-600">Emails Opened</div>
										</div>
										<div className="p-4 rounded-lg bg-default-100">
											<div className="text-2xl font-bold">{selectedCampaign.status.clicked_links}</div>
											<div className="text-sm text-default-600">Links Clicked</div>
										</div>
										<div className="p-4 rounded-lg bg-default-100">
											<div className="text-2xl font-bold">{selectedCampaign.status.submitted_data}</div>
											<div className="text-sm text-default-600">Data Submitted</div>
										</div>
									</div>
									<div className="mt-4">
										<div className="mb-2">Campaign Progress</div>
										<Progress
											aria-label="Campaign progress"
											value={(selectedCampaign.status.sent_emails / selectedCampaign.status.total_emails) * 100}
											color={getProgressColor((selectedCampaign.status.sent_emails / selectedCampaign.status.total_emails) * 100)}
											className="w-full"
										/>
									</div>
								</div>
							) : (
								<div className="text-center py-4">
									<Spinner size="lg" />
								</div>
							)}
						</ModalBody>
						<ModalFooter>
							<Button color="primary" onPress={onStatsClose}>
								Close
							</Button>
						</ModalFooter>
					</ModalContent>
				</Modal>
			</div>
		</DefaultLayout>
	);
}
