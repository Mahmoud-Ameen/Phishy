import api from "./api";
import { API_ENDPOINTS } from "../config/api";

export interface Campaign {
    id: number;
    name: string;
    start_date: string;
    started_by: string;
    scenario_id: number;
}

export interface PhishingEmail {
    id: number;
    recipient_email: string;
    sent_at: string | null;
    status: string;
    error_message: string | null;
    campaign_id: number;
    template_id: number;
    created_at: string;
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
        status: CampaignStatus;
        emails?: PhishingEmail[];
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
            const response = await api.get<CampaignsResponse>(API_ENDPOINTS.campaigns, {
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
            const response = await api.post<CampaignResponse>(
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

    async getCampaign(campaignId: number): Promise<CampaignResponse> {
        try {
            const token = localStorage.getItem("token");
            const headers = token ? { Authorization: `Bearer ${token}` } : {};
            const response = await api.get<CampaignResponse>(
                `${API_ENDPOINTS.campaigns}/${campaignId}`,
                { headers }
            );
            return response.data;
        } catch (error) {
            console.error("Error fetching campaign:", error);
            throw error;
        }
    }
};
