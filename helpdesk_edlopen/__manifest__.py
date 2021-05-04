# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Helpdesk Eduardo López",
    "version": "14.0.1.0.0",
    "author": "AEODOO, Odoo Community Association (OCA)",
    "maintainers": ["edlopen"],
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "wizards/create_ticket_view.xml",
        "views/helpdesk_menu.xml",
        "views/helpdesk_views.xml",
        "views/helpdesk_ticket_tag_views.xml",
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "data/cron.xml",
    ],
}
