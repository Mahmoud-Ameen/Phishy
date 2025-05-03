from flask import request, Response
from .resources.repository import ResourceRepository

def serve_phishing_resource():
    """Before request hook to serve dynamic phishing resources."""
    # Exclude known application/API paths
    if request.path.startswith('/api/'):
        return None # Let Flask handle it normally

    domain = request.host.split(':')[0] # Remove port if present
    endpoint = request.path

    # Attempt to find a matching resource
    # Ensure the repository method is accessible/correctly imported
    resource = ResourceRepository.get_resource_by_domain_and_endpoint(domain, endpoint)

    if resource:
        # TODO: Add interaction tracking logic here
        print(f"Serving dynamic resource from hook for domain: {domain}, path: {endpoint}")
        return Response(
            resource.content,
            mimetype=resource.content_type
        )
    
    # If no resource found, continue to normal routing (which might lead to 404)
    return None 