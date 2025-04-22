Table phishing_scenarios {
id int [primary key, unique, increment]
name varchar [not null]
description text
level int
}

Table email_templates {
id int [primary key, unique]
scenario_id int [not null, ref: > phishing_scenarios.id]
subject varchar [not null]
body text [not null]
sender_account_id int [not null, ref: > sender_accounts.id]
placeholders text[]
}

// For now assume only usage of one sender account hardcoded in the code
Table sender_accounts {
id int [primary key, unique]
email_address varchar [not null, unique]
smtp_server varchar [not null]
smtp_port int [not null]
username varchar [not null]
encrypted_password text [not null]  
}

Table domains {
domain_name varchar [primary key, not null, unique]
is_active boolean [default:true]
}

Table phishing_resources {
id int [primary key, unique]
scenario_id int [not null, ref: > phishing_scenarios.id]
domain_name int [not null, ref: > domains.domain_name]
endpoint varchar [not null] // e.g., "/login"
content text [not null] // HTML content
content_type varchar [not null] // text/html, image/png, etc.
created_at timestamp
}

Table phishing_targets {
tracking_key uuid [primary key, not null, unique] // Unique tracking key
phishing_email_id int [ref:> email_templates.id]
target_identity string [unique, default:"unknown"] // would be email if targeted through email, unkown if no tracking key is specified
// phishing email_id is nullable to allow targeting people using channels other than emails in the future
}

Table phishing_emails {
id int [primary key, unique]
template_id int [not null, ref: > email_templates.id]
target_id int [not null, ref: > phishing_targets.id]
status enum("pending", "sent", "failed") [not null]
sent_at timestamp
}

Table phishing_interactions {
id int [primary key, unique]
tracking_key uuid [not null, ref: > phishing_targets.tracking_key]
phishing_resource_id int [not null, ref: > phishing_resources.id]
interaction_type enum("click", "page_visit", "form_submit") [not null]
ip_address varchar [not null]
user_agent text
timestamp timestamp
}
