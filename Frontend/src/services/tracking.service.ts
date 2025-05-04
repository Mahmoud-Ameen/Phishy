import api from './api';

// Interface for a single interaction record
export interface Interaction {
    id: number;
    tracking_key: string;
    interaction_type: 'email_open' | 'resource_visit' | 'submission' | string; 
    ip_address: string;
    user_agent: string | null;
    interaction_metadata: string | null;
    timestamp: string; // ISO date string
}

interface InteractionsResponse {
    data: {
        interactions: Interaction[];
    };
    message: string;
    status: string;
}


const trackingService = {
    /**
     * Fetches all interactions for a given tracking key (UUID).
     * @param trackingKey The UUID associated with a phishing email.
     * @returns Promise containing the API response with interactions.
     */
    getInteractions: async (trackingKey: string): Promise<Interaction[]> => {
        try {
            const headers = { authorization: `Bearer ${localStorage.getItem('token')}` };
            const response = (await api.get<InteractionsResponse>(`/api/tracking/interactions/${trackingKey}`, { headers })).data.data;
            return response.interactions;
        } catch (error) {
            console.error('Error fetching interactions:', error);
            throw error;
        }
    },
};

export { trackingService }; 