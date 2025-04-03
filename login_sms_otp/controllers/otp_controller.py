from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
import logging
import time
from odoo.tools.translate import _
from .otp_service import OTPService  # Importing service from a separate file
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db, _get_login_redirect_url, is_user_internal

_logger = logging.getLogger(__name__)

SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email'}
class OTPController(Home):
    """Controller to handle OTP-based login."""

    login_parameters = {}

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        """Handle login and OTP authentication."""
        ensure_db()
        request.params['login_success'] = False
        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        if request.httprequest.method == 'POST':
            try:
                auth_result = OTPService.authenticate_user(request)
                if not auth_result:
                    return request.redirect('/login?error=invalid_credentials')
                user_id, otp_enabled = auth_result
                if not otp_enabled:
                    uid = request.session.authenticate(request.db, request.params['login'], request.params['password'])
                    request.params['login_success'] = True
                    return request.redirect(self._login_redirect(uid))
                else:
                    request.session['check_otp_user'] = user_id
                    self.login_parameters = {
                        'login': request.params['login'],
                        'password': request.params['password']
                    }
                    OTPService.generate_and_store_otp(user_id)
                    return request.redirect('/login/otp')
            except AccessDenied as e:
                if e.args == AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')
        return super(OTPController, self).web_login(redirect=redirect, **kw)

    @http.route('/login/otp', type='http', auth='public', website=True)
    def otp_form(self, **kw):
        """Render OTP form."""
        if not request.session.get('check_otp_user'):
            return request.redirect('/web/login?error=Session expired, please log in again')

        _logger.info("Rendering OTP form for user: %s", request.session.get('check_otp_user'))
        return request.render('login_sms_otp.otp_template')

    @http.route('/otp/validate', type='json', auth='public', methods=['POST'])
    def validate_otp(self, **kwargs):
        """Validate the entered OTP."""
        entered_otp = kwargs.get('otp')
        if not request.session.get('otp') or int(time.time()) > request.session.get('otp_expiry', 0):
            return {"error": _("OTP expired, please request a new one")}

        if entered_otp == request.session['otp']:
            _logger.info("OTP validated successfully for user: %s", request.session.get('check_otp_user'))
            uid = request.session.authenticate(request.db, self.login_parameters['login'],
                                               self.login_parameters['password'])
            OTPService.clear_otp_session()
            self.login_parameters = {}
            request.params['login_success'] = True
            return request.redirect(self._login_redirect(uid))

        _logger.warning("Invalid OTP attempt for user: %s", request.session.get('check_otp_user'))
        request.session['failed_otp_attempts'] = request.session.get('failed_otp_attempts', 0) + 1
        return {"error": _("Invalid OTP")}

    @http.route('/otp/resend', type='json', auth='public', methods=['POST'])
    def resend_otp(self, **kwargs):
        """Resend OTP."""
        user_id = request.session.get('check_otp_user')
        if not user_id:
            return {"error": _("Session expired. Please log in again.")}

        if request.session.get('resend_attempts', 0) >= 5:
            _logger.warning("Too many OTP resend attempts for user: %s", user_id)
            return {"error": _("Too many OTP resend attempts. Try again later.")}

        request.session['resend_attempts'] = request.session.get('resend_attempts', 0) + 1
        _logger.info("Resending OTP for user: %s", user_id)
        OTPService.generate_and_store_otp(user_id)
        return {"success": True, "message": _("OTP resent successfully. Please check your SMS.")}

    def _login_redirect(self, uid, redirect=None):
        return _get_login_redirect_url(uid, redirect)