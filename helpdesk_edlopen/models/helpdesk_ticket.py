from odoo import _, api, fields, models


class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'

    name = fields.Char()

    date = fields.Date()

    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket'
    )


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Helpdesk tag'

    name = fields.Char()
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        string='Tickets'
    )


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
        compute='_compute_assigned'
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

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to'
    )

    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions'
    )

    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        relation='helpdesk_ticket_tag_rel',
        colum1='ticket_id',
        colum2='tag_id',
        string='Tags'
    )

    ticket_qty = fields.Integer(
        string='Ticket Qty',
        compute='_compute_ticket_qty'
    )

    tag_name = fields.Char(string='Tag Name')

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

    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            #record.assigned = record.user_id and True or False
            record.assigned = record.user_id.exists()

    def _compute_ticket_qty(self):
        for record in self:
            record.user_id
            other_tickets = self.env['helpdesk.ticket'].search([('user_id', '=', record.user_id.id)])
            record.ticket_qty = len(other_tickets)

    def create_tag(self):
        self.ensure_one()
        # opción 1
        self.write({
            'tag_ids': [(0, 0, {'name': self.tag_name})]
        })
        # opción 2
        tag = self.env['helpdesk.ticket.tag'].create({
            'name': self.tag_name
        })
        self.write({
            'tag_ids': [(4, tag.id, 0)]
        })
        # opción 3
        tag = self.env['helpdesk.ticket.tag'].create({
            'name': self.tag_name
        })
        self.write({
            'tag_ids': [(6, 0, tag.ids)]
        })
        # opción 4
        tag = self.env['helpdesk.ticket.tag'].create({
            'name': self.tag_name,
            'ticket_ids': [(6, 0, self.ids)]
        })
        # finalmente limpiamos el contenido de tag_name
        self.tag_name = False