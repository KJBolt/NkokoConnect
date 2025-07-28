from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
from datetime import timedelta

_logger = logging.getLogger(__name__)


class Reminders(models.Model):
    _name = 'reminders'
    _description = 'Reminders'
    _order = 'id desc'
    _inherit = ['mail.thread']

    user_id = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True, index=True)
    farmer_id = fields.Many2one('farmers', string='Farmer', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=False, tracking=True)
    feeding_plan = fields.Selection(
        [
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        string='Feeding Plan',
        required=True
    )
    next_feeding_date = fields.Date(string="Next Feeding Date", required=True)
    vaccination_plan = fields.Selection(
        [
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        string='Vaccination Plan',
        required=True
    )
    next_vaccination_date = fields.Date(string="Next Vaccination Date", required=True)
    feeding_message = fields.Char(string="Feeding Message", required=True)
    vaccination_message = fields.Char(string="Vaccination Message", required=True)


    # Filter records based on user
    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        user = self.env.user
        
        # If user is admin, don't apply any filters
        if user.has_group('base.group_system'):
            return super(Reminders, self).search(args or [], offset=offset, limit=limit, order=order)
        
        # For regular users, filter only their records
        args = args or []
        args = ['|', ('user_id', '=', user.id), ('user_id', '=', False)] + args
        
        return super(Reminders, self).search(args, offset=offset, limit=limit, order=order)


    # Check if farmer has phone number
    @api.constrains('next_feeding_date', 'next_vaccination_date')
    def _check_if_farmer_has_phone_no(self):
        for record in self:
            if not record.farmer_id.phone_number:
                raise UserError("Farmer's phone number is required to send alerts. Please update the farmer's phone number in Contacts module")


    # Set state to completed when record is created
    @api.model_create_multi
    def create(self, vals_list):
        # Ensure we handle both single and multiple record creation
        for vals in vals_list:
            vals['status'] = 'ongoing'
            self.send_sms_notification()
        return super(Reminders, self).create(vals_list)


    # Set state to completed when record is updated
    def write(self, vals):
        res = super(Reminders, self).write(vals)
        # Only modify status if it's not being set to draft via set_to_draft
        if 'status' in vals and vals['status'] == 'draft' and not self._context.get('set_to_draft'):
            vals['status'] = 'ongoing'
        # Only set to completed if status is not being set at all
        elif 'status' not in vals and not self._context.get('set_to_draft'):
            vals['status'] = 'ongoing'
        self.send_sms_notification()
        return res


    # Set to draft
    def set_to_draft(self):
        # Use the ORM to update the status with a context flag
        self.with_context(set_to_draft=True).write({'status': 'draft'})
        return True


    # Cancel reminder
    def cancel_reminder(self):
        self.write({'status': 'cancelled'})
        return True


    # if status is ongoing you cannot delete the record
    def unlink(self):
        for record in self:
            if record.status == 'ongoing':
                raise UserError("You cannot delete a record that is in the Ongoing. First cancel the reminder.")
        return super(Reminders, self).unlink()


    # Send sms notification to user based of feeding plan and next feeding date
    def send_sms_notification(self):
        for record in self:
            if record.status != 'ongoing' or not record.farmer_id.phone_number:
                continue

            # Send immediate notification if today is the feeding date
            today = fields.Date.today()
            if record.next_feeding_date == today:
                message = (
                    f"Nkoko Connect - Feeding Reminder\n"
                    f"Date: {today.strftime('%A, %B %d, %Y')}\n\n"
                    f"{record.feeding_message or 'Time to feed your birds!'}\n\n"
                    f"Thank you for using Nkoko Connect!"
                )
                self._send_sms(
                    phone=record.farmer_id.phone_number,
                    message=message
                )

            # Schedule next reminder based on the plan
            next_date = self._get_next_reminder_date(record.feeding_plan, record.next_feeding_date)
            if next_date:
                record.next_feeding_date = next_date
                _logger.info(f"Next feeding reminder scheduled for {next_date}")


    # Get next reminder date
    def _get_next_reminder_date(self, plan_type, current_date):
        """Calculate the next reminder date based on the plan type"""
        if not current_date:
            return False
            
        if plan_type == 'daily':
            return current_date + timedelta(days=1)
        elif plan_type == 'weekly':
            return current_date + timedelta(weeks=1)
        elif plan_type == 'monthly':
            # Add approximately one month (using 30 days as an approximation)
            return current_date + timedelta(days=30)
        return False


    # Send SMS notification
    def _send_sms(self, phone, message):
        """Helper method to send SMS"""
        try:
            # Replace this with your actual SMS gateway integration
            # This is a placeholder for the SMS sending logic
            _logger.info(f"Sending SMS to {phone}: {message}")
            # Example: sms_gateway = self.env['sms.gateway']
            # sms_gateway.send_sms(phone, message)
            return True
        except Exception as e:
            _logger.error(f"Failed to send SMS: {str(e)}")
            return False


    # Cron job to send scheduled reminders
    @api.model
    def _cron_send_scheduled_reminders(self):
        """Cron job to send scheduled reminders"""
        _logger.info("Running cron job to send scheduled reminders")
        today = fields.Date.today()
        reminders = self.search([
            ('status', '=', 'ongoing'),
            ('next_feeding_date', '<=', today),
        ])
        
        for reminder in reminders:
            try:
                reminder.send_sms_notification()
            except Exception as e:
                _logger.error(f"Error processing reminder {reminder.id}: {str(e)}")