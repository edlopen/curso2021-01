from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError


class HelpdeskTicketAction(models.Model):
    _name = 'helpdesk.ticket.action'
    _description = 'Action'

    name = fields.Char()

    date = fields.Date()

    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
        string='Ticket'
    )

    time = fields.Float(
        string='Time'
    )


class HelpdeskTicketTag(models.Model):
    _name = 'helpdesk.ticket.tag'
    _description = 'Helpdesk tag'

    name = fields.Char()
    ticket_ids = fields.Many2many(
        comodel_name='helpdesk.ticket',
        string='Tickets'
    )

    @api.model 
    def cron_delete_tag(self):
        tickets = self.search([('ticket_ids','=',False)])
        tickets.unlink()

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Ticket'
    _inherit = [
        'mail.thread.cc',
        'mail.thread.blacklist',
        'mail.activity.mixin',
    ]
    _primary_email = 'email_from'

    def _date_default_today(self):
        return fields.Date.today()

    def _default_user_id(self):
        return self.env.uid

    name = fields.Char(
        string='Name',
        required=True
    )

    description = fields.Text(
        string="Description"
    )

    date = fields.Date(
        string='Date',
        default=_date_default_today
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
        string='Dedicated Time',
        compute='_get_time',
        inverse='_set_time',
        search='_search_time',
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
        string='Assigned to',
        default=_default_user_id,
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
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

    color = fields.Integer(
        string='Color',
        default=0
    )

    email_from = fields.Char()

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
        """
        #import pdb; pdb.set_trace()
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
        """
        action = self.env.ref('helpdesk_edlopen.helpdesk_ticket_create_tag_action').read()[0]
        action['context'] = {
            'default_name':self.tag_name,
            'default_ticket_ids':[(6, 0, self.ids)]
        }
        return action

    @api.constrains('dedicated_time')
    def _verify_dedicated_time (self):
        """dedicated_time debe ser siempre positivo"""
        for ticket in self:
            if ticket.dedicated_time < 0:
                raise ValidationError (_("Dedicated time cannot be negative." ))

    @api.onchange('date')
    def _onchange_date(self):
        """date_limit is set as one day more than date field"""
        for ticket in self.filtered(lambda t: t.date):
            ticket.date_limit = ticket.date + timedelta(days=1)

    @api.depends('action_ids.time')
    def _get_time(self):
        for record in self:
            # sumatorio del tiempo de todas las acctiones
            total_time = sum(record.action_ids.mapped('time'))

    def _set_time(self):
        for record in self.filtered(lambda r: r.dedicated_time):
            time_now = sum(record.action_ids.mapped('time'))
            next_time = record.dedicated_time - time_now
            if next_time:
                data = {
                    'name': '/',
                    'time': next_time,
                    'date': fields.Date.today(),
                    'ticket_id': record.id,
                }
                self.env['helpdesk.ticket.action'].create(data)

    def _search_time(self, operator, value):
        actions = self.env['helpdesk.ticket.action'].search([('time', operator, value)])
        return [('id', 'in', actions.mapped('ticket_id').ids)]