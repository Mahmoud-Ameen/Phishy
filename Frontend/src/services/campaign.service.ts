import axios from "axios";
import { API_ENDPOINTS } from "../config/api";

export interface Campaign {
    id: number;
    name: string;
    start_date: string;
    started_by: string;
    scenario_id: number;
}

export interface CampaignStatus {
    total_emails: number;
    sent_emails: number;
    opened_emails: number;
    clicked_links: number;
    submitted_data: number;
}

interface CampaignsResponse {
    data: {
        campaigns: Campaign[];
    };
    message: string;
    status: string;
}

interface CampaignResponse {
    data: {
        campaign: Campaign;
    };
    message: string;
    status: string;
}

interface CampaignStatusResponse {
    data: {
        status: CampaignStatus;
    };
    message: string;
    status: string;
}

export interface StartCampaignData {
    name: string;
    scenario_id: number;
    employee_emails: string[]
}

export const campaignService = {
    async getCampaigns(): Promise<CampaignsResponse> {
        try {
            const token = localStorage.getItem("token");
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const response = await axios.get<CampaignsResponse>(API_ENDPOINTS.campaigns, {
                headers,
            });
            return response.data;
        } catch (error) {
            console.error("Error fetching campaigns:", error);
            throw error;
        }
    },

    async startCampaign(data: StartCampaignData): Promise<CampaignResponse> {
        try {
            const token = localStorage.getItem("token");
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const response = await axios.post<CampaignResponse>(
                API_ENDPOINTS.campaigns,
                data,
                { headers }
            );
            return response.data;
        } catch (error) {
            console.error("Error starting campaign:", error);
            throw error;
        }
    },

    async getCampaignStatus(campaignId: number): Promise<CampaignStatusResponse> {
        try {
            const token = localStorage.getItem("token");
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const response = await axios.get<CampaignStatusResponse>(
                `${API_ENDPOINTS.campaigns}/${campaignId}/status`,
                { headers }
            );
            return response.data;
        } catch (error) {
            console.error("Error fetching campaign status:", error);
            throw error;
        }
    },
};
