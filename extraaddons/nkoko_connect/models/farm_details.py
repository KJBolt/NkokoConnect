from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)


class FarmDetails(models.Model):
    _name = 'farm.details'
    _description = 'Farm Details'
    _rec_name = 'farm_name'
    _order = 'id desc'
    _inherit = ['mail.thread']

    farmer_id = fields.Many2one('farmers', string='Farmer', required=True)
    farm_name = fields.Char(string='Name of Farm', required=False)
    farm_type = fields.Selection([
        ('layers', 'Layers'), 
        ('boilers', 'Boilers'),
        ('mixed', 'Mixed'),
    ], 
    string='Farm Type', 
    required=True)

    current_stock = fields.Integer(string='Total No of Birds', required=True)
    max_capacity = fields.Integer(string='Farm Bird Capacity', required=False)
    housing_type = fields.Selection([
        ('deep_litter', 'Deep Litter'),
        ('battery_cage', 'Battery Cage'),
        ('free_range', 'Free Range'),
    ], 
    string='Housing Type', 
    required=False)

    feed_source = fields.Selection([
        ('self_milled', 'Self Milled'),
        ('local_supplier', 'Local Supplier'),
        ('Coop', 'Coop'),
    ], 
    string='Feed Source', 
    required=False)

    water_source = fields.Selection([
        ('borehole', 'Borehole'),
        ('tap', 'Tap'),
        ('rainwater', 'Rainwater'),
        ('river', 'River'),
    ], 
    string='Water Source', 
    required=False)

    biosecurity_measures = fields.Text(string='Biosecurity Measures', required=False)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('completed', 'Completed'),
    ], 
    string='Status',
    default='draft', 
    required=False)


    # Create Farm Details
    @api.model_create_multi
    def create(self, vals_list):
        # Ensure we handle both single and multiple record creation
        for vals in vals_list:
            vals['status'] = 'completed'
        return super(FarmDetails, self).create(vals_list)


    def write(self, vals):
        # Only modify status if it's not being set to draft via set_to_draft
        if 'status' in vals and vals['status'] == 'draft' and not self._context.get('set_to_draft'):
            vals['status'] = 'completed'
        # Only set to completed if status is not being set at all
        elif 'status' not in vals and not self._context.get('set_to_draft'):
            vals['status'] = 'completed'
        return super(FarmDetails, self).write(vals)


    # Set to draft
    def set_to_draft(self):
        logger.info(f"Set to draft => {self.status}")
        # Use the ORM to update the status with a context flag
        self.with_context(set_to_draft=True).write({'status': 'draft'})
        return True
