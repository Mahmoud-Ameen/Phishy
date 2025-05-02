import api from './api';
import { API_ENDPOINTS } from '../config/api';

export interface Domain {
    domain_name: string;
    is_active: boolean;
}

interface DomainsResponse {
    data: Domain[];
    message: string;
    status: string;
}

interface CreateDomainResponse {
    data: Domain;
    message: string;
    status: string;
}

const domainService = {
    getDomains: async (): Promise<Domain[]> => {
        try {
            const response = await api.get<DomainsResponse>(API_ENDPOINTS.domains);
            // Check if response.data exists and has a data property which is an array
            if (response.data && Array.isArray(response.data.data)) {
                return response.data.data;
            } else {
                console.error('Invalid response structure for getDomains:', response.data);
                // Return empty array or throw error based on how you want to handle this
                return []; 
            }
        } catch (error) {
            console.error('Failed to fetch domains:', error);
            throw error; // Re-throw the error to be handled by the caller
        }
    },

    createDomain: async (domainName: string): Promise<Domain> => {
        try {
            const response = await api.post<CreateDomainResponse>(API_ENDPOINTS.domains, { domain_name: domainName });
            // Check if response.data exists and has a data property
            if (response.data && response.data.data) {
                return response.data.data;
            } else {
                 console.error('Invalid response structure for createDomain:', response.data);
                 // Throw an error as creation implies a specific return object expected
                 throw new Error('Failed to create domain due to invalid server response.');
            }
        } catch (error) {
            console.error('Failed to create domain:', error);
            throw error; // Re-throw the error
        }
    },
};

export default domainService; 