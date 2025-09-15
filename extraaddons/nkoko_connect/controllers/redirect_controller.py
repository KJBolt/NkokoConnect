from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TestController(http.Controller):
    
    @http.route('/mofa', type='http', auth="public", website=True)
    def mofa_route(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', request.session.get('login'))], limit=1)
        if user:
            if user.user_role == 'farmer' or user.user_role == 'supplier' or user.user_role == 'admin':
                return request.redirect('/page-restriction')

            else:
                return request.redirect('/web')

        else:
            _logger.warning("No user found in session for /mofa endpoint")
            return request.redirect('/web/login')


    @http.route('/farmer', type='http', auth="public", website=True)
    def farmer_route(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', request.session.get('login'))], limit=1)
        if user:
            if user.user_role == 'farmer':
                # Simplest approach: just redirect to the web client
                # This will take the user to their dashboardt user
                
                # First, find the farmer record for this user
                farmer = request.env['farmers'].sudo().search([('full_name', '=', user.partner_id.id)], limit=1)
                
                if farmer:
                    _logger.info(f"Found farmer record for user {user.login}: {farmer.id}")
                    
                    # Get the action
                    action = request.env.ref('nkoko_connect.action_farmers').sudo()
                    action_id = action.id
                    model = action.res_model
                    
                    # Redirect to the specific farmer record instead of a filtered list
                    redirect_url = f"/web#id={farmer.id}&action={action_id}&model={model}&view_type=form"
                    
                    return f"""
                        <!DOCTYPE html>
                        <html>
                            <head>
                                <title>Redirecting...</title>
                                <script type="text/javascript">
                                    window.top.location.href = '{redirect_url}';
                                </script>
                            </head>
                        </html>
                    """
                else:
                    _logger.warning(f"No farmer record found for user {user.login} with partner_id {user.partner_id.id}")
                    # Fallback to the standard view without filtering
                    action = request.env.ref('nkoko_connect.action_farmers').sudo()
                    redirect_url = f"/web#action={action.id}&model={action.res_model}&view_type=list"
                    
                    return f"""
                        <!DOCTYPE html>
                        <html>
                            <head>
                                <title>Redirecting...</title>
                                <script type="text/javascript">
                                    window.top.location.href = '{redirect_url}';
                                </script>
                            </head>
                        </html>
                    """
            else:
                return request.redirect('/web/login')
        else:
            return request.redirect('/web/login')



    @http.route('/procurement', type='http', auth="public", website=True)
    def procurement_route(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', request.session.get('login'))], limit=1)
        if user:
            _logger.info(f"User {user.login} has role: {user.user_role}")
            if user.user_role == 'supplier':
                _logger.info("User role is supplier - access granted")
                # Add your supplier-specific logic here
                return request.redirect('/web')  # or wherever supplier users should go
            else:
                _logger.warning(f"User {user.login} with role '{user.user_role}' attempted to access /procurement endpoint")
                return request.redirect('/web/login')
        else:
            _logger.warning("No user found in session for /procurement endpoint")
            return request.redirect('/web/login')


    @http.route('/admin', type='http', auth="public", website=True)
    def admin_route(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', request.session.get('login'))], limit=1)
        if user:
            _logger.info(f"User {user.login} has role: {user.user_role}")
            if user.user_role == 'admin':
                _logger.info("User role is admin - access granted")
                # Add your admin-specific logic here
                return request.redirect('/web')  # or wherever admin users should go
            else:
                _logger.warning(f"User {user.login} with role '{user.user_role}' attempted to access /admin endpoint")
                return request.redirect('/web/login')
        else:
            _logger.warning("No user found in session for /admin endpoint")
            return request.redirect('/web/login')