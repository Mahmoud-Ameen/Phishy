I think most use cases we are considering right now fall into one of two categories

1. Setup phase
   admin adds company employees. (Company Service)
   The admin registers a new domain. (Phishing Service)
   Creates email templates or phishing resources. (Phishing Service)
   Creates a phishing scenario. (Phishing Service)
2. Execution phase
   Admin wants to start a campaign. (Company + Phishing)
   Admin provides campaign name, scenario_id to be used, and selects a set of employees.
   Campaigns, as a concept is related to the company service not the phishing service.
   The company service receives the campaign request, creates a campaign entity in its database, and tells the phishing service to send phishing emails using teh scenario with scenario_id to those emails.
   Phishing service:
   for each email,
   create a phishing email record with status pending
   ask the tracking module to generate a tracking key for this phishing_email
   parse the email template replacing every {{tracking_key}} with the email tracking key
   send the email
   mark it as sent.
