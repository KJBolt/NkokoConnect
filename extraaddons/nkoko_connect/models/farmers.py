from odoo import models, fields, api

class Farmers(models.Model):
    _name = 'farmers'
    _description = "Farmers"
    _rec_name = 'full_name'

    user_id = fields.Char(string="User ID", required=True, default=lambda self: self.env['ir.sequence'].next_by_code('farmers'))
    full_name = fields.Many2one('res.partner', string="Full Name", required=True)
    phone_number = fields.Char(related='full_name.phone', string="Phone Number", required=False)
    pin_code = fields.Char(string="Pin Code", required=False)
    prefered_language = fields.Selection([('english', 'English'), ('ewe', 'Ewe'), ('twi', 'Twi')], string="Prefered Language", required=True)
    account_status = fields.Selection([('active', 'Active'), ('suspended', 'Suspended'), ('incomplete', 'Incomplete')], string="Account Status", required=True)
    registration_source = fields.Selection([('ussd', 'USSD'), ('web', 'Web'), ('agent', 'Agent'), ('app', 'App')], string="Registration Source", required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    photo = fields.Image(string="Photo", required=True)
    national_id_type = fields.Selection([('voter_id', 'Voter ID'), ('ghana_card', 'Ghana Card'), ('passport', 'Passport')], string="National ID Type", required=True)
    national_id_number = fields.Char(string="National ID Number", required=True)
    education_level = fields.Selection([('none', 'None'), ('primary', 'Primary'), ('secondary', 'Secondary'), ('tertiary', 'Tertiary')], string="Education Level", required=True)
    farming_experience_years = fields.Char(string="Years of poultry farming experience", required=True)
    region = fields.Char(string="Region", required=True)
    district = fields.Char(string="District", required=True)
    community = fields.Char(string="Community", required=True)
    gps_location = fields.Char(string="GPS Location", required=True)