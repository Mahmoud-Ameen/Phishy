import api from './api';
import { API_ENDPOINTS } from '../config/api';

export interface Resource {
    id: number;
    scenario_id: number;
    domain_name: string;
    endpoint: string;
    content: string;
    content_type: string;
    created_at?: string; // Assuming ISO string format from backend
}

// Interface for the data structure when creating a resource
export interface CreateResourceData {
    scenario_id: number;
    domain_name: string;
    endpoint: string;
    content: string;
    content_type: string;
}

// Expected response structure from the backend for list operations
interface ResourcesResponse {
    data: Resource[];
    message: string;
    status: string;
}

// Expected response structure for single resource/creation operations
interface ResourceResponse {
    data: Resource;
    message: string;
    status: string;
}


const resourceService = {
    // Get resources for a specific scenario
    getResourcesByScenario: async (scenarioId: number): Promise<Resource[]> => {
        try {
            const response = await api.get<ResourcesResponse>(`${API_ENDPOINTS.resources}/scenario/${scenarioId}`);
             // Check if response.data exists and has a data property which is an array
            if (response.data && Array.isArray(response.data.data)) {
                return response.data.data;
            } else {
                console.error('Invalid response structure for getResourcesByScenario:', response.data);
                return []; 
            }
        } catch (error) {
            console.error(`Failed to fetch resources for scenario ${scenarioId}:`, error);
            throw error;
        }
    },

    // Create a new resource
    createResource: async (resourceData: CreateResourceData): Promise<Resource> => {
        try {
            const response = await api.post<ResourceResponse>(API_ENDPOINTS.resources, resourceData);
            // Check if response.data exists and has a data property
            if (response.data && response.data.data) {
                return response.data.data;
            } else {
                 console.error('Invalid response structure for createResource:', response.data);
                 throw new Error('Failed to create resource due to invalid server response.');
            }
        } catch (error) {
            console.error('Failed to create resource:', error);
            throw error;
        }
    },
    
};

export default resourceService; 