import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DefaultLayout from "@/layouts/default";
import {
    Card,
    CardBody,
    CardHeader,
    Divider,
    Chip,
    Table,
    TableHeader,
    TableColumn,
    TableBody,
    TableRow,
    TableCell,
    Button,
    Progress,
    Spinner,
    Tooltip,
} from "@heroui/react";
import { Campaign, CampaignStatus, PhishingEmail, campaignService } from "@/services/campaign.service";
import { Scenario, scenarioService } from "@/services/scenario.service";
import { ArrowLeftIcon, EnvelopeIcon, CheckCircleIcon, XCircleIcon, ClockIcon, ExclamationCircleIcon } from "@heroicons/react/24/outline";
import { toast } from "react-toastify";

export default function CampaignDetailsPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const campaignId = parseInt(id || "0");
    
    const [loading, setLoading] = useState(true);
    const [campaign, setCampaign] = useState<Campaign | null>(null);
    const [scenario, setScenario] = useState<Scenario | null>(null);
    const [status, setStatus] = useState<CampaignStatus | null>(null);
    const [phishingEmails, setPhishingEmails] = useState<PhishingEmail[]>([]);
    const [error, setError] = useState<string | null>(null);
    
    useEffect(() => {
        if (campaignId) {
            fetchCampaignData();
        }
    }, [campaignId]);
    
    const fetchCampaignData = async () => {
        setLoading(true);
        setError(null);
        
        try {
            // Get all campaign data from a single endpoint
            const campaignResponse = await campaignService.getCampaign(campaignId);
            const { campaign, status, emails = [] } = campaignResponse.data;
            
            // Set campaign data
            setCampaign(campaign);
            setStatus(status);
            setPhishingEmails(emails);
            
            // Get scenario details if available
            if (campaign?.scenario_id) {
                try {
                    const scenarioResponse = await scenarioService.getScenario(campaign.scenario_id);
                    setScenario(scenarioResponse.data.scenario);
                } catch (error) {
                    console.error("Error fetching scenario details:", error);
                }
            }
        } catch (error) {
            console.error("Error fetching campaign data:", error);
            setError("Failed to load campaign data. Please try again later.");
            toast.error("Failed to load campaign data");
        } finally {
            setLoading(false);
        }
    };
    
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleString();
    };
    
    const getStatusChip = (status: string) => {
        switch (status) {
            case "pending":
                return <Chip startContent={<ClockIcon className="h-4 w-4" />} color="warning" size="sm">Pending</Chip>;
            case "sent":
                return <Chip startContent={<EnvelopeIcon className="h-4 w-4" />} color="primary" size="sm">Sent</Chip>;
            case "opened":
                return <Chip startContent={<CheckCircleIcon className="h-4 w-4" />} color="success" size="sm">Opened</Chip>;
            case "clicked":
                return <Chip startContent={<CheckCircleIcon className="h-4 w-4" />} color="success" size="sm">Clicked</Chip>;
            case "submitted":
                return <Chip startContent={<CheckCircleIcon className="h-4 w-4" />} color="success" size="sm">Submitted</Chip>;
            case "failed":
                return <Chip startContent={<XCircleIcon className="h-4 w-4" />} color="danger" size="sm">Failed</Chip>;
            default:
                return <Chip startContent={<ExclamationCircleIcon className="h-4 w-4" />} color="default" size="sm">{status}</Chip>;
        }
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
    
    if (error || !campaign) {
        return (
            <DefaultLayout>
                <div className="px-6 py-4">
                    <div className="flex items-center mb-6">
                        <Button
                            variant="light"
                            startContent={<ArrowLeftIcon className="h-4 w-4" />}
                            onPress={() => navigate("/campaigns")}
                            className="mr-4">
                            Back to Campaigns
                        </Button>
                        <h1 className="text-3xl font-semibold text-[#0077B6]">
                            Campaign Details
                        </h1>
                    </div>
                    
                    <div className="bg-red-50 p-6 rounded-lg text-center">
                        <p className="text-red-600 mb-4">
                            {error || "Campaign not found"}
                        </p>
                        <Button color="primary" onPress={() => navigate("/campaigns")}>
                            Return to Campaigns
                        </Button>
                    </div>
                </div>
            </DefaultLayout>
        );
    }
    
    return (
        <DefaultLayout>
            <div className="px-6 py-4">
                <div className="flex items-center mb-6">
                    <Button
                        variant="light"
                        startContent={<ArrowLeftIcon className="h-4 w-4" />}
                        onPress={() => navigate("/campaigns")}
                        className="mr-4">
                        Back to Campaigns
                    </Button>
                    <h1 className="text-3xl font-semibold text-[#0077B6]">
                        {campaign.name}
                    </h1>
                </div>
                
                <div className="grid grid-cols-12 gap-6">
                    {/* Campaign Overview */}
                    <Card className="col-span-12 lg:col-span-4">
                        <CardHeader className="flex justify-between">
                            <h2 className="text-xl font-semibold">Campaign Overview</h2>
                            <Chip size="sm" color="primary">ID: {campaign.id}</Chip>
                        </CardHeader>
                        <Divider />
                        <CardBody className="space-y-4">
                            <div>
                                <div className="text-small text-default-500">Started By</div>
                                <div>{campaign.started_by}</div>
                            </div>
                            <div>
                                <div className="text-small text-default-500">Start Date</div>
                                <div>{formatDate(campaign.start_date)}</div>
                            </div>
                            <div>
                                <div className="text-small text-default-500">Scenario</div>
                                <div className="flex items-center">
                                    {scenario?.name || `Scenario ${campaign.scenario_id}`}
                                    {scenario?.level && (
                                        <Chip
                                            size="sm"
                                            color={scenario.level > 2 ? "danger" : "warning"}
                                            className="ml-2">
                                            Level {scenario.level}
                                        </Chip>
                                    )}
                                </div>
                                {scenario?.description && (
                                    <div className="text-small text-default-500 mt-1">
                                        {scenario.description}
                                    </div>
                                )}
                            </div>
                        </CardBody>
                    </Card>
                    
                    {/* Statistics */}
                    <Card className="col-span-12 lg:col-span-8">
                        <CardHeader>
                            <h2 className="text-xl font-semibold">Campaign Statistics</h2>
                        </CardHeader>
                        <Divider />
                        <CardBody>
                            {status ? (
                                <div className="space-y-6">
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                        <div className="p-4 rounded-lg bg-default-100">
                                            <div className="text-2xl font-bold">{status.total_emails}</div>
                                            <div className="text-sm text-default-600">Total Emails</div>
                                        </div>
                                        <div className="p-4 rounded-lg bg-default-100">
                                            <div className="text-2xl font-bold">{status.sent_emails}</div>
                                            <div className="text-sm text-default-600">Emails Sent</div>
                                        </div>
                                        <div className="p-4 rounded-lg bg-default-100">
                                            <div className="text-2xl font-bold">{status.opened_emails}</div>
                                            <div className="text-sm text-default-600">Emails Opened</div>
                                        </div>
                                        <div className="p-4 rounded-lg bg-default-100">
                                            <div className="text-2xl font-bold">{status.clicked_links}</div>
                                            <div className="text-sm text-default-600">Links Clicked</div>
                                        </div>
                                    </div>
                                    
                                    <div>
                                        <div className="flex justify-between text-small mb-1">
                                            <span>Campaign Progress</span>
                                            <span className="text-foreground/50">
                                                {Math.round((status.sent_emails / status.total_emails) * 100)}%
                                            </span>
                                        </div>
                                        <Progress
                                            aria-label="Campaign progress"
                                            value={(status.sent_emails / status.total_emails) * 100}
                                            color={getProgressColor((status.sent_emails / status.total_emails) * 100)}
                                            className="w-full"
                                        />
                                    </div>
                                </div>
                            ) : (
                                <div className="text-center p-4">No statistics available</div>
                            )}
                        </CardBody>
                    </Card>
                    
                    {/* Phishing Emails Table */}
                    <Card className="col-span-12">
                        <CardHeader>
                            <h2 className="text-xl font-semibold">Phishing Emails</h2>
                        </CardHeader>
                        <Divider />
                        <CardBody>
                            <Table aria-label="Phishing emails for campaign">
                                <TableHeader>
                                    <TableColumn>RECIPIENT</TableColumn>
                                    <TableColumn>STATUS</TableColumn>
                                    <TableColumn>SENT TIME</TableColumn>
                                    <TableColumn>CREATED TIME</TableColumn>
                                    <TableColumn>ERROR</TableColumn>
                                </TableHeader>
                                <TableBody>
                                    {phishingEmails.length > 0 ? (
                                        phishingEmails.map((email) => (
                                            <TableRow key={email.id}>
                                                <TableCell>{email.recipient_email}</TableCell>
                                                <TableCell>{getStatusChip(email.status)}</TableCell>
                                                <TableCell>
                                                    {email.sent_at ? formatDate(email.sent_at) : "-"}
                                                </TableCell>
                                                <TableCell>{formatDate(email.created_at)}</TableCell>
                                                <TableCell>
                                                    {email.error_message ? (
                                                        <Tooltip content={email.error_message}>
                                                            <Button size="sm" variant="light" color="danger">
                                                                View Error
                                                            </Button>
                                                        </Tooltip>
                                                    ) : "-"}
                                                </TableCell>
                                            </TableRow>
                                        ))
                                    ) : (
                                        <TableRow>
                                            <TableCell colSpan={5}>
                                                <div className="text-center p-4">No phishing emails found</div>
                                            </TableCell>
                                        </TableRow>
                                    )}
                                </TableBody>
                            </Table>
                        </CardBody>
                    </Card>
                </div>
            </div>
        </DefaultLayout>
    );
} 