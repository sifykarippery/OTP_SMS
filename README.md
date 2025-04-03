


## Problem Statement 
- Implement a feature in Odoo 16 Community Edition where users receive a One-Time Password
(OTP) via SMS upon login. The login process should proceed only after successful OTP verification.
- Only users with this option enabled should be required to enter an OTP upon login.


## How to work Flow-User Documention
- Login User Configure
![Login OTP Configure](/login_sms_otp/static/src/img/otp_login_enabled.png )
- OTP Page
![OTP Page](/login_sms_otp/static/src/img/otp_login_enabled.png "Render page for otp")
- User enter Invalid otp
![Invalid otp](/login_sms_otp/static/src/img/invalid_otp.png " enter Invalid otp")
![Enable resend ](/login_sms_otp/static/src/img/resend_otp.png "after the cooldown time Resend otp will send")

## Things to improve

1.Lack of Odoo IAP credits for testing. Instead, use a free service provider like Twilio for testing but included both code.





