$(document).ready(function () {
    "use strict";

    /*==================================
* Author        : "ThemeSine"
* Template Name :  HTML Template
* Version       : 1.0
==================================== */

    /*=========== TABLE OF CONTENTS ===========
1. Scroll To Top 
======================================*/

    // 1. Scroll To Top
    $(window).on("scroll", function () {
        if ($(this).scrollTop() > 600) {
            $(".return-to-top").fadeIn();
        } else {
            $(".return-to-top").fadeOut();
        }
    });
    $(".return-to-top").on("click", function () {
        $("html, body").animate(
            {
                scrollTop: 0,
            },
            1500
        );
        return false;
    });
});

$(function () {
    if (document.cookie.match("ssid")) {
        window.location.replace("/layout"); // TODO: redirect to index
    }
    $("#register").click(() => {
        if (!$("#styled-checkbox-2").prop("checked")) {
            alert("请同意《用户协议》");
            return;
        }
        if (!$("#password-form").val().match(/[0-9a-zA-Z]{6,}/)) {
            alert("密码不符合格式：6位以上的字母和数字");
        }
        if ($("#password-form").val() == $("#password-form-repeat").val()) {
            $.post(
                "http://127.0.0.1:5000/api/register",
                {
                    username: $("#username-form").val(),
                    password: $("#password-form").val(),
                },
                function (data, textStatus, jqXHR) {
                    if (data.status_code == 0) {
                        window.location.replace("/tosignin"); // TODO: redirect to index
                    } else {
                        if (data.status_code == 1) {
                            alert("用户名已被注册");
                            $("#username-form").val("");
                        } else if (data.status_code == 2) {
                        }
                    }
                },
                "json"
            );
        }
    });
});
