odoo.define('web_sms_otp.otp_verification', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.OtpVerification = publicWidget.Widget.extend({
        selector: '#otp_form', // Ensure this matches your form ID or class
        events: {
            'submit': '_onSubmitOTP',
            'click #resend_otp': '_onResendOTP',
        },

        start: function () {
            this._startTimer(60); // Start 2-minute timer on page load
            return this._super.apply(this, arguments);
        },

      _onSubmitOTP: function (event) {
    event.preventDefault();

    var otpInput = this.$("#otp_code").val();
    var errorContainer = this.$("#otp_error");

    this._rpc({
        route: "/otp/validate",
        params: { otp: otpInput },
    }).then((result) => {
        if (result.error) {
            errorContainer.text(result.error).show();
        } else {
            errorContainer.hide();
            if (result.redirect) {
                window.location.href = result.redirect;
            }
        }
    });
},
        _startTimer: function (duration) {
            let self = this;
            let timerElement = this.$("#timer");
            let resendButton = this.$("#resend_otp");

            let remaining = duration;

            function updateTimer() {
                if (remaining < 0) {
                    resendButton.prop('disabled', false); // Enable Resend OTP Button
                    timerElement.text("00:00");
                    return;
                }

                let m = Math.floor(remaining / 60);
                let s = remaining % 60;
                timerElement.text((m < 10 ? "0" + m : m) + ":" + (s < 10 ? "0" + s : s));
                remaining--;

                setTimeout(updateTimer, 1000);
            }

            resendButton.prop('disabled', true); // Disable Resend OTP Button initially
            updateTimer();
        },

        _onResendOTP: function (event) {
            event.preventDefault();
            var self = this;
            let otp_success_message = this.$("#otp_success");
            let errorContainer = this.$("#otp_error");

            // Call the backend to resend OTP
            this._rpc({
                route: '/otp/resend',
                params: {},
            }).then(function (response) {
                if (response.success) {
                     otp_success_message.text(response.message).show();
                     errorContainer.text(response.message).hide();

                    // Show success message
                    self._startTimer(60);
                } else {
                    otp_success_message.text(response.message).hide()
                    alert(response.error);  // Show error message
                }
            });
        },
    });

    return publicWidget.registry.OtpVerification;
});