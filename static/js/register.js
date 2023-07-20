// get verification code bottom
function getVerificationBtnClick() {
    $("#ver-btn").on("click", function(event) {
        var $this = $(this); // the same as #ver-btn
        var email = $("input[name='email']").val();
        if (!email) {
            alert("Please enter the email first!");
            return;
        }
        // sending the request through js: ajax
        $.ajax({
            url: "/user/verification",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                var code = res['code'];
                if (code == 200) {
                    // cancel click event
                    $this.off("click");
                    // start the countdown
                    var countDown = 60;
                    var timer = setInterval(function () {
                        countDown -= 1;
                        if (countDown > 0) {
                            $this.text("Retry after " + countDown + "s");
                        } else {
                            $this.text("Get the Code");
                            // apply the function, activate the click event
                            getVerificationBtnClick();
                            // no need for countdown, clear it
                            clearInterval(timer);
                        }
                    }, 1000);
                    alert("Verification Code sent successfully!");
                } else {
                    alert(res['message']);
                }
            }
        })
    });
}

// wait the whole element in the website loaded, then continue to run
$(function () {
    getVerificationBtnClick();
});
