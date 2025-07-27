from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)

class FarmerDashboard(models.Model):
    _name = 'farmer.dashboard'
    _description = 'Farmer Dashboard'
    _order = 'id desc'
    _inherit = ['mail.thread']

    # expense_total = fields.Float(string="Total Expense", compute='_compute_expense_total', store=True)
    # revenue_total = fields.Float(string="Total Revenue", compute='_compute_revenue_total', store=True)

    # @api.depends()
    # def _compute_expense_total(self):
    #     # Get all paid customer invoices
    #     paid_invoices = self.env['account.move'].search([
    #         ('move_type', '=', 'out_invoice'),  # Sales invoices
    #         ('payment_state', 'in', ['paid', 'in_payment']),  # Paid or in payment
    #         ('state', '=', 'posted')  # Posted invoices only
    #     ])
        
    #     # Calculate total amount from all paid invoices
    #     total = sum(invoice.amount_total_signed for invoice in paid_invoices)
        
    #     # Update the expense_total field
    #     self.expense_total = total


    # @api.depends()
    # def _compute_revenue_total(self):
    #     # Get all paid vendor bills
    #     paid_bills = self.env['account.move'].search([
    #         ('move_type', '=', 'in_invoice'),  # Vendor bills
    #         ('payment_state', 'in', ['paid', 'in_payment']),  # Paid or in payment
    #         ('state', '=', 'posted')  # Posted bills only
    #     ])
        
    #     # Calculate total amount from all paid bills
    #     total = sum(bill.amount_total_signed for bill in paid_bills)
        
    #     # Update the revenue_total field
    #     self.revenue_total = total