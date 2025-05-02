import React, { useState, useEffect } from 'react';
import domainService, { Domain } from '../../services/domain.service';
import { PlusIcon } from '@heroicons/react/24/solid';
import { toast } from 'react-toastify';

const DomainsPage: React.FC = () => {
    const [domains, setDomains] = useState<Domain[]>([]);
    const [newDomainName, setNewDomainName] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [isAdding, setIsAdding] = useState<boolean>(false);

    useEffect(() => {
        fetchDomains();
    }, []);

    const fetchDomains = async () => {
        setIsLoading(true);
        try {
            const fetchedDomains = await domainService.getDomains();
            setDomains(fetchedDomains);
        } catch (error) {       
            toast.error('Failed to load domains.');
            console.error('Failed to fetch domains:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleAddDomain = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newDomainName.trim()) {
            toast.warn('Domain name cannot be empty.');
            return;
        }
        setIsAdding(true);
        try {
            const newDomain = await domainService.createDomain(newDomainName.trim());
            setDomains([...domains, newDomain]);
            setNewDomainName(''); // Clear input field
            toast.success(`Domain ${newDomain.domain_name} added successfully!`);
        } catch (error: any) {
            // Check for specific backend error messages if available
            const errorMessage = error.response?.data?.message || 'Failed to add domain.';
            toast.error(errorMessage);
            console.error('Failed to add domain:', error);
        } finally {
            setIsAdding(false);
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-6 text-gray-800">Manage Domains</h1>

            {/* Add Domain Form */}
            <form onSubmit={handleAddDomain} className="mb-8 p-4 border rounded shadow-sm bg-white">
                <h2 className="text-xl font-semibold mb-3">Add New Domain</h2>
                <div className="flex items-center space-x-3">
                    <input
                        type="text"
                        value={newDomainName}
                        onChange={(e) => setNewDomainName(e.target.value)}
                        placeholder="e.g., example-phish.com"
                        className="flex-grow px-3 py-2 border border-gray-300 rounded shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={isAdding}
                    />
                    <button
                        type="submit"
                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded inline-flex items-center transition duration-150 ease-in-out disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={isAdding}
                    >
                        <PlusIcon className="h-5 w-5 mr-2" />
                        {isAdding ? 'Adding...' : 'Add Domain'}
                    </button>
                </div>
            </form>

            {/* Domain List Table */}
            <div className="bg-white shadow-md rounded overflow-hidden">
                <h2 className="text-xl font-semibold p-4 border-b">Existing Domains</h2>
                {isLoading ? (
                    <p className="p-4 text-center text-gray-500">Loading domains...</p>
                ) : (
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Domain Name
                                </th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                    Status
                                </th>
                                {/* Add Actions column if needed later */}
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {domains.length === 0 ? (
                                <tr>
                                    <td colSpan={2} className="px-6 py-4 text-center text-gray-500">No domains found.</td>
                                </tr>
                            ) : (
                                domains.map((domain) => (
                                    <tr key={domain.domain_name}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            {domain.domain_name}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                                            <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${domain.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                                {domain.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        {/* Add action buttons (edit/delete) here if needed */}
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default DomainsPage; 