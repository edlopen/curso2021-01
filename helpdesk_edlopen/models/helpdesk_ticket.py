from odoo import fields, models


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'

    name = fields.Char(
        string='Name',
        required=True
    )
    description = fields.Text(
        string="Description"
    )
    date = fields.Date(
        string='Date'
    )
    state = fields.Selection([
        ('new', 'New'),
        ('assigned','Assigned'),
        ('in_process','In process'),
        ('pending','Pending'),
        ('solved','Solved'),
        ('canceled','Canceled'),],
        default='new',
        string='State'
    )
    dedicated_time = fields.Float(
        string='Dedicated Time'
    )
    assigned = fields.Boolean(
        string='Assigned',
        required=True
    )
    date_limit = fields.Date(
        string='Date Limit'
    )
    action_corrective = fields.Html(
        string='Corrective Action',
        help='Descrive corrective actions to do.'
    )
    action_preventive = fields.Html(
        string='Preventive Action',
        help='Descrive preventive actions to do.'
    )
