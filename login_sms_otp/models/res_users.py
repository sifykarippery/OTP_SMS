# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions,_


class LoginUserInherit(models.Model):
    _inherit = "res.users"

    otp_sms_enable=fields.Boolean("Login OTP SMS")





