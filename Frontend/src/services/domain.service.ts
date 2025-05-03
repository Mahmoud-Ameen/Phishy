import api from './api';
import { API_ENDPOINTS } from '../config/api';

export interface Domain {
    domain_name: string;
    is_active: boolean;
}

interface DomainsResponse {
    data: {domains: Domain[]};
    message: string;
    status: string;
}

interface CreateDomainResponse {
    data: {domain: Domain};
    message: string;
    status: string;
}

const domainService = {
    getDomains: async (): Promise<Domain[]> => {
        try {
            const response = await api.get<DomainsResponse>(API_ENDPOINTS.domains);
            // Check if response.data exists and has a data property which is an array
            if (response.data && Array.isArray(response.data.data.domains)) {
                return response.data.data.domains;
            } else {
                console.error('Invalid response structure for getDomains:', response.data);
                return []; 
            }
        } catch (error) {
            console.error('Failed to fetch domains:', error);
            throw error; // Re-throw the error to be handled by the caller
        }
    },

    createDomain: async (domainName: string): Promise<Domain> => {
        try {
            const headers = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
            const response = await api.post<CreateDomainResponse>(API_ENDPOINTS.domains, { domain_name: domainName }, { headers });
            // Check if response.data exists and has a data property
            if (response.data && response.data.data) {
                return response.data.data.domain;
            } else {
                 console.error('Invalid response structure for createDomain:', response.data);
                 throw new Error('Failed to create domain due to invalid server response.');
            }
        } catch (error) {
            console.error('Failed to create domain:', error);
            throw error; 
        }
    },
};

export default domainService; 