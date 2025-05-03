from flask import request, Response
from .resources.repository import ResourceRepository
from .tracking.service import TrackingService

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
        # Track the resource visit
        try:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            # Extract tracking key from query param if present (e.g., ?tid=<key>)
            tracking_key = request.args.get('tid') 

            # Record interaction 'resource_visit'
            if tracking_key:
                TrackingService.track_interaction(
                    tracking_key=tracking_key,
                    interaction_type='resource_visit',
                    ip_address=ip_address,
                    user_agent=user_agent
                )
            else:
                # Handle visits without a tracking key (e.g., direct access)
                print(f"Untracked resource visit: {domain}{endpoint} from {ip_address}")
                
        except Exception as e:
            # Log error but continue serving resource
            print(f"Error during resource visit tracking: {e}")

        print(f"Serving dynamic resource from hook for domain: {domain}, path: {endpoint}")
        return Response(
            resource.content,
            mimetype=resource.content_type
        )
    
    # If no resource found, continue to normal routing (which might lead to 404)
    return None 