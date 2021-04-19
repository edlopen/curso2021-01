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

    def action_assigned(self):
        self.ensure_one()
        self.write({
            'state': 'assigned',
            'assigned': True
        })

    def action_in_process(self):
        self.ensure_one()
        self.state = 'in_process'

    def action_pending(self):
        self.ensure_one()
        self.state = 'pending'

    def action_solved(self):
        self.ensure_one()
        self.state = 'solved'

    def action_canceled(self):
        self.ensure_one()
        self.state = 'canceled'