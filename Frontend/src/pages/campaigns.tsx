import { useEffect, useState, useMemo } from "react";
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
	useDisclosure,
	Chip,
	Spinner,
	Progress,
	ButtonGroup,
} from "@heroui/react";
import { PlusIcon, ChartBarIcon, EyeIcon } from "@heroicons/react/24/outline";
import { useNavigate } from "react-router-dom";
import { Campaign, CampaignStatus, campaignService } from "@/services/campaign.service";
import { Scenario, scenarioService } from "@/services/scenario.service";
import { toast } from "react-toastify";

interface CampaignWithData extends Campaign {
	scenario?: Scenario;
	status?: CampaignStatus;
}

export default function CampaignPage() {
	const navigate = useNavigate();
	const { isOpen: isStatsOpen, onOpen: onStatsOpen, onClose: onStatsClose } = useDisclosure();
	const [campaigns, setCampaigns] = useState<CampaignWithData[]>([]);
	const [loading, setLoading] = useState(true);
	const [selectedCampaign, setSelectedCampaign] = useState<CampaignWithData | null>(null);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		fetchCampaigns();
	}, []);

	const fetchCampaigns = async () => {
		setLoading(true);
		setError(null);
		
		try {
			// Get all campaigns
			const campaignsResponse = await campaignService.getCampaigns();
			const campaignsList = campaignsResponse.data.campaigns;
			
			// Since we're using a single endpoint for campaign detail/status, we don't need all the parallel
			// fetching or a cache. Just set the basic campaigns list.
			setCampaigns(campaignsList);
		} catch (error) {
			console.error("Error fetching campaigns:", error);
			setError("Failed to load campaigns. Please try again later.");
			toast.error("Failed to load campaigns");
		} finally {
			setLoading(false);
		}
	};

	const handleViewStats = async (campaign: CampaignWithData) => {
		try {
			// Fetch full campaign details 
			const campaignResponse = await campaignService.getCampaign(campaign.id);
			setSelectedCampaign({
				...campaign,
				status: campaignResponse.data.status
			});
			onStatsOpen();
		} catch (error) {
			console.error("Error fetching campaign details:", error);
			toast.error("Failed to load campaign details");
		}
	};

	const formatDate = (dateString: string) => {
		return new Date(dateString).toLocaleDateString();
	};

	const getProgressColor = (percentage: number) => {
		if (percentage < 30) return "danger";
		if (percentage < 70) return "warning";
		return "success";
	};

	// Sort campaigns by start date (newest first)
	const sortedCampaigns = useMemo(() => {
		return [...campaigns].sort((a, b) => 
			new Date(b.start_date).getTime() - new Date(a.start_date).getTime()
		);
	}, [campaigns]);

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

				{error && (
					<div className="p-4 mb-4 bg-red-100 text-red-700 rounded-lg">
						{error}
					</div>
				)}

				{campaigns.length === 0 && !error ? (
					<div className="text-center p-8 bg-default-100 rounded-lg">
						<p className="text-default-600 mb-4">No campaigns found.</p>
						<Button 
							color="primary" 
							onPress={() => navigate("/campaigns/create")}>
							Create Your First Campaign
						</Button>
					</div>
				) : (
					<Table aria-label="Phishing campaigns">
						<TableHeader>
							<TableColumn>NAME</TableColumn>
							<TableColumn>SCENARIO</TableColumn>
							<TableColumn>START DATE</TableColumn>
							<TableColumn>ACTIONS</TableColumn>
						</TableHeader>
						<TableBody>
							{sortedCampaigns.map((campaign) => (
								<TableRow key={campaign.id}>
									<TableCell>{campaign.name}</TableCell>
									<TableCell>
										{campaign.scenario?.name || `Scenario ${campaign.scenario_id}`}
									</TableCell>
									<TableCell>{formatDate(campaign.start_date)}</TableCell>
									<TableCell>
										<ButtonGroup>
											<Button
												color="secondary"
												variant="light"
												size="sm"
												startContent={<ChartBarIcon className="h-4 w-4" />}
												onPress={() => handleViewStats(campaign)}>
												Stats
											</Button>
											<Button
												color="primary"
												variant="light"
												size="sm"
												startContent={<EyeIcon className="h-4 w-4" />}
												onPress={() => navigate(`/campaigns/${campaign.id}`)}>
												Details
											</Button>
										</ButtonGroup>
									</TableCell>
								</TableRow>
							))}
						</TableBody>
					</Table>
				)}

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
							<Button 
								color="secondary" 
								variant="light" 
								onPress={() => navigate(`/campaigns/${selectedCampaign?.id}`)}>
								View Details
							</Button>
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
