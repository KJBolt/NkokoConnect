from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class TestController(http.Controller):
    
    @http.route('/mofa', type='http', auth="public", website=True)
    def mofa_route(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', request.session.get('login'))], limit=1)
        if user:
            if user.user_role == 'mofa':
                _logger.info("User role is mofa")
            else:
                return request.redirect('/web/login')
        else:
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
            if user.user_role == 'supplier':
                _logger.info("User role is supplier")
            else:
                return request.redirect('/web/login')
        else:
            return request.redirect('/web/login')


    @http.route('/admin', type='http', auth="public", website=True)
    def admin_route(self, **kw):
        user = request.env['res.users'].sudo().search([('login', '=', request.session.get('login'))], limit=1)
        if user:
            if user.user_role == 'admin':
                _logger.info("User role is admin")
            else:
                return request.redirect('/web/login')
        else:
            return request.redirect('/web/login')