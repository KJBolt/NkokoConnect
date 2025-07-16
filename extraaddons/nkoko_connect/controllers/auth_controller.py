from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import logging

_logger = logging.getLogger(__name__)

class AuthSignupExtended(AuthSignupHome):
    def do_signup(self, qcontext):
        # Get the request parameters
        params = request.params if request else qcontext.get('params', {})
        
        # Get values from both qcontext and params
        values = {
            'phone_no': qcontext.get('phone_no') or params.get('phone_no'),
            'user_role': qcontext.get('user_role') or params.get('user_role'),
            'region': qcontext.get('region') or params.get('region'),
        }
        
        _logger.info("Processing signup with values: %s", values)
        
        # Call parent to create the user
        result = super(AuthSignupExtended, self).do_signup(qcontext)
        
        # Get the newly created user and update additional fields
        login = qcontext.get('login') or params.get('login')
        _logger.info("Login value: %s", login)
        
        if login:
            user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
            _logger.info("Found user: %s", user)
            if user:
                # Get group references
                group_portal = request.env.ref('base.group_portal')
                group_user = request.env.ref('base.group_user')
                group_farmer = request.env.ref('nkoko_connect.group_farmer')
                group_mofa = request.env.ref('nkoko_connect.group_mofa')
                group_supplier = request.env.ref('nkoko_connect.group_supplier')
                
                # Prepare group assignments
                group_commands = []
                
                # Determine user type and assign appropriate groups
                if values.get('user_role') in ['farmer', 'mofa', 'supplier']:
                    # Internal User with specific role group
                    group_commands.append((4, group_user.id))  # Add Internal User
                    group_commands.append((3, group_portal.id))  # Remove Portal User
                    
                    # Add specific role group
                    if values['user_role'] == 'farmer':
                        group_commands.append((4, group_farmer.id))
                        group_commands.append((3, group_mofa.id))
                        group_commands.append((3, group_supplier.id))
                    elif values['user_role'] == 'mofa':
                        group_commands.append((4, group_mofa.id))
                        group_commands.append((3, group_farmer.id))
                        group_commands.append((3, group_supplier.id))
                    elif values['user_role'] == 'supplier':
                        group_commands.append((4, group_supplier.id))
                        group_commands.append((3, group_farmer.id))
                        group_commands.append((3, group_mofa.id))
                else:
                    # Portal User
                    group_commands.append((4, group_portal.id))  # Add Portal User
                    group_commands.append((3, group_user.id))    # Remove Internal User
                    # Remove all role groups
                    group_commands.extend([
                        (3, group_farmer.id),
                        (3, group_mofa.id),
                        (3, group_supplier.id)
                    ])
                
                # Update user with all changes
                user.write({
                    'groups_id': group_commands,
                    'phone_no': values['phone_no'],
                    'user_role': values['user_role'],
                    'region': values['region']
                })
                
                _logger.info("Updated user with values: %s and groups: %s", values, group_commands)
        
        return result