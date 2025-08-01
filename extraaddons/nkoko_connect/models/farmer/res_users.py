from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    user_role = fields.Selection(
        selection=[
            ('user', 'User'),
            ('admin', 'Admin'),
            ('farmer', 'Farmer'),
            ('mofa', 'MOFA'),
            ('supplier', 'Supplier'),
        ],
        string='User Role',
    )

    phone_no = fields.Char(string='Phone Number')
    region = fields.Selection(
        selection=[
            ('greater_accra', 'Greater Accra'),
            ('ashanti', 'Ashanti'),
            ('brong_ahafo', 'Brong Ahafo'),
            ('central', 'Central'),
            ('eastern', 'Eastern'),
            ('northern', 'Northern'),
            ('upper_east', 'Upper East'),
            ('upper_west', 'Upper West'),
            ('western', 'Western'),
            ('western_north', 'Western North'),
            ('volta', 'Volta'),
            ('ofoase', 'Ofoase'),
            ('bono_east', 'Bono East'),
            ('savannah', 'Savannah'),
            ('north_east', 'North East'),
            ('akim', 'Akim')
        ],
        string='Region'
    )