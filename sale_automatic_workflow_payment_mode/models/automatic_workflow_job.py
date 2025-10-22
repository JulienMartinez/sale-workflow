# © 2016 Camptocamp SA, Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AutomaticWorkflowJob(models.Model):
    _inherit = "automatic.workflow.job"

    def _prepare_dict_account_payment(self, invoice):
        vals = super()._prepare_dict_account_payment(invoice)
        
        payment_mode = None
        if (invoice.preferred_payment_method_line_id and 
            invoice.preferred_payment_method_line_id.payment_mode_id):
            payment_mode = invoice.preferred_payment_method_line_id.payment_mode_id
            
        if payment_mode:
            vals["payment_type"] = payment_mode.payment_type
            if payment_mode.payment_method_id:
                vals["payment_method_id"] = payment_mode.payment_method_id.id
            if payment_mode.fixed_journal_id:
                vals["journal_id"] = payment_mode.fixed_journal_id.id
        return vals

    def _register_payment_invoice(self, invoice):
        payment_mode = None
        if (invoice.preferred_payment_method_line_id and 
            invoice.preferred_payment_method_line_id.payment_mode_id):
            payment_mode = invoice.preferred_payment_method_line_id.payment_mode_id
            
        if payment_mode and not payment_mode.fixed_journal_id:
            _logger.debug(
                "Unable to Register Payment for invoice %s: "
                "Payment mode %s must have fixed journal",
                invoice.id,
                payment_mode.id,
            )
            return False
        return super()._register_payment_invoice(invoice)