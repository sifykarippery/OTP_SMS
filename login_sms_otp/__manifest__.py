# -*- coding: utf-8 -*-
{
    'name': "Login_otp_sms",

    'summary': """
        Odoo login SMS OTP for selected user
        """,

    'description': """
    OTP Verification (SMS)

    This module adds an extra layer of security by enabling OTP-based SMS verification during user login.

    Once enabled, users will receive a 6-digit One-Time Password (OTP) via SMS on their registered mobile number.

    Access to the system will only be granted after successful OTP verification.
    """
    ,

    'author': "Sify Karippery Raphy",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_users_inherit.xml',
        'views/login_otp_templates.xml',
        'data/login_otp_sms_template.xml'
    ],
'assets': {
        'web.assets_frontend': [
            'login_sms_otp/static/src/js/login_sms_otp.js',
        ],

    },
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'license': 'LGPL-3',

}
