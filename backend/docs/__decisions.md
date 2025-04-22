Phishing Awareness Campaign Automation - System Overview
📌 Project Summary
This project is an automated phishing awareness campaign system designed to help organizations test and educate their employees about phishing threats. It consists of two main services:

Admin Dashboard & Management Service – Manages companies, employees, phishing scenarios, and campaign configurations.
Phishing Server – Sends phishing emails, serves phishing pages, and tracks user interactions.
The system provides custom phishing scenarios, tracks user interactions, and generates detailed reports for security awareness training.

The phishing service is divided into the following modules:

1️⃣ emails/ - Email Management & Sending
Stores email templates with placeholders.
Manages sender accounts (SMTP/API-based sending).
Requests tracking keys from tracking/.
Replaces placeholders and sends phishing emails.
Tracks email status (pending, sent, failed).
2️⃣ scenario/ - Phishing Scenario Management
Stores phishing scenarios (email templates & phishing pages).
Links domains to phishing pages.
Dynamically serves phishing content based on domain + endpoint.
3️⃣ tracking/ - Target Management & Interaction Tracking
Generates tracking keys for phishing targets.
Logs who interacted (clicked a link, visited a page, entered credentials).
Associates interactions with phishing campaigns for reporting.

Design Decisions
We are following a feature-based folder structure. Each group of related features is placed in a folder.
Each feature/module follows a layered architecture:

-   routes (API routes if applicable)
-   controller (business logic)
-   service (core logic)
-   repository (abstraction layer for database abstracting underlyign ORM/database)
-   models (database models currently using SQLAlchemy)
-   entities (domain entities serve as abstraction over database models, returned from repository layer and used in service and controller layers)
