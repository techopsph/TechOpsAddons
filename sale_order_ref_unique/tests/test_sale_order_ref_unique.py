from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class SaleOrderRefUnique(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(SaleOrderRefUnique, cls).setUpClass()
        cls.sale_order_model = cls.env["sale.order"]
        cls.sale_order = cls.sale_order_model.create(
            {"name": "S0-ORDER-TEST", "client_order_ref": "SOA123456789"}
        )

    def test_duplicated_sale_order_ref_creation(self):
        with self.assertRaises(ValidationError):
            self.sale_order_model.with_context(test_sale_order_ref=True).create(
                {"name": "S0-ORDER-TEST", "client_order_ref": "SOA123456789"}
            )

    def test_duplicate_sale_order(self):
        sale_order_copied = self.sale_order.copy()
        self.assertFalse(sale_order_copied.vat)
