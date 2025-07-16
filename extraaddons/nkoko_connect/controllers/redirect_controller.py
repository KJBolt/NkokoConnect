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
                # Get the action
                action = request.env.ref('nkoko_connect.action_farmers').sudo()
                action_id = action.id
                model = action.res_model

                # Construct proper redirect URL
                redirect_url = f"/web#action={action_id}&model={model}&view_type=list"
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