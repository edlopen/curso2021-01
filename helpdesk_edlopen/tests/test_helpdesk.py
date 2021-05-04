from odoo.tests.common import TransactionCase

from odoo.exceptions import ValidationError


class TestHelpdesk(TransactionCase):

    def setUp(self):
        super().setUp()

        self.ticket = self.env['helpdesk.ticket'].create({
            'name': 'test ticket',
            'dedicated_time': 500.0,
        })

    def test_01_ticket(self):
        self.assertEqual(self.ticket.name, 'test ticket')

    def test_02_ticket(self):
        self.assertEqual(self.ticket.user_id.id, self.uid)

    def test_03_ticket(self):
        self.assertFalse(self.ticket.name == 'test')

    def test_04_ticket(self):
        """TEST 04:
        Check time exception
        """
        self.ticket.dedicated_time = 2
        self.assertEqual(self.ticket.dedicated_time, 2)
        self.ticket.dedicated_time = 0
        self.assertEqual(self.ticket.dedicated_time, 0)
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.ticket.dedicated_time = -7