# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    workflow_process_id = fields.Many2one(
        compute="_compute_workflow_process_id", store=True, readonly=False
    )

    @api.depends(
        "payment_method_line_id",
        "payment_method_line_id.workflow_process_id",
    )

    def _compute_workflow_process_id(self):
        for sale in self:
            sale.workflow_process_id = (
                sale.payment_method_line_id.workflow_process_id
                if sale.payment_method_line_id
                else False
            )