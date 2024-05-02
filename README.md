# Project-Status-Sheet

## Description
The Project Status Sheet (PSS) is an enterprise module designed for SAAS platforms using Odoo. It automates the generation and emailing of detailed project reports, reducing manual efforts by 50%. The module sends weekly email reports automatically to customers, project followers, and project managers, significantly reducing the administrative burden on project managers and ensuring timely updates on project status.

## Key Features
- **Automated Email Reports**: Sends detailed project status reports as PDF attachments to project stakeholders, including customers, project followers, and project managers every week.
- **Reduced Manual Effort**: Automates what was previously a manual process, cutting down the effort required by project managers to keep stakeholders informed.
- **Customizable Templates**: Utilizes customizable email and PDF report templates that can be adjusted according to project or organizational needs.

## Technical Details
### Models
- `project.project`: Enhanced to include a boolean field `is_pss_sent` that tracks whether the project status sheet should be sent.

### Methods
- `action_pss_send()`: Opens a wizard to compose an email with the project status report attached as a PDF.
- `_send_email_pss_cron()`: A scheduled job that sends out the project status reports automatically on a weekly basis.

### Server Actions
- **Update Project to Invoice**: An action that updates projects to be ready for invoicing, reflecting the dynamic nature of project tracking and billing.

### Automation
- A cron job is set up to execute `_send_email_pss_cron` every 7 days, ensuring that reports are sent out automatically without manual intervention.

## Installation Instructions
To install the Project Status Sheet module, follow these steps:

1. Ensure you have a working installation of Odoo and access to the SAAS platform's server.
2. Clone this repository to your machine:
git clone https://github.com/yourusername/project-status-sheet.git
3. Add the module to your Odoo addons path:
--addons-path=/path/to/your/addons,/path/to/project-status-sheet
4. Update your Odoo module list and install the module from the Odoo backend interface.

## Usage
Once installed, the module will automatically send a weekly project status report to the designated stakeholders. Reports are generated based on the latest project data and sent every Monday at 6:30 AM server time.


