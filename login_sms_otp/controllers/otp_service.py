import xmlrpc.client
import random
import time
import logging
from odoo.http import request
from odoo import _
from . twilio_service import TwilioSMSService

_logger = logging.getLogger(__name__)


class OTPService:
    """Service class to handle OTP-related operations."""

    # @staticmethod
    # def authenticate_user(request):
    #     """Authenticate user using XML-RPC and check OTP status."""
    #     odoo_url = request.httprequest.host_url
    #     db = request.db
    #     username = request.params.get('login')
    #     password = request.params.get('password')
    #
    #     _logger.info("Authenticating user: %s", username)
    #
    #     common = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common")
    #     user_id = common.authenticate(db, username, password, {})
    #
    #     if not user_id:
    #         _logger.warning("Authentication failed for user: %s", username)
    #         return None
    #
    #     models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")
    #     user_data = models.execute_kw(
    #         db, user_id, password,
    #         'res.users', 'read',
    #         [user_id],
    #         {'fields': ['otp_sms_enable']}
    #     )
    #
    #     otp_enabled = user_data[0]['otp_sms_enable'] if user_data else False
    #     _logger.info("User %s OTP status: %s", username, otp_enabled)
    #     return user_id, otp_enabled

    @staticmethod
    def generate_and_store_otp(user_id):
        """Generate and store OTP in session."""
        otp = str(random.randint(100000, 999999))
        expiry_time = int(time.time()) + 120
        user = request.env['res.users'].browse(user_id)

        try:
            partner_language = user.sudo().lang or 'en_US'
            request.env['sms.sms'].sudo().with_context(lang=partner_language).create({
                'partner_id': user.sudo().partner_id.id,
                'number': user.sudo().partner_id.mobile,
                'body': _("Odoo login OTP: %s") % otp,
                'state': 'outgoing'
            })._send()
            # TwilioSMSService.send_sms(user.sudo().partner_id.id,message="Odoo login OTP: %s" % otp)
            _logger.info("OTP sent successfully to user: %s", user_id)
            _logger.info("OTP sent successfully to user: %s",otp )
        except Exception as e:
            _logger.error("Failed to send OTP to user: %s, Error: %s", user_id, str(e))

        request.session.update({
            'otp': otp,
            'otp_expiry': expiry_time
        })
        _logger.debug("Generated OTP: %s for user: %s", otp, user_id)

    @staticmethod
    def clear_otp_session():
        """Clear OTP session data."""
        for key in ['otp', 'otp_expiry', 'check_otp_user', 'failed_otp_attempts']:
            request.session.pop(key, None)
        _logger.info("Cleared OTP session data")