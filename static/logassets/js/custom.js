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
    $("#username-form").val(localStorage.getItem("username"));
    $("#password-form").val(localStorage.getItem("password"));
    if (localStorage.getItem("password") != null) {
        $("#styled-checkbox-2").prop("checked", true);
    }
    $("#login").click(() => {
        if ($("#styled-checkbox-2").prop("checked")) {
            localStorage.setItem("username", $("#username-form").val());
            localStorage.setItem("password", $("#password-form").val());
        } else {
            localStorage.removeItem("username");
            localStorage.removeItem("password");
        }
        $.post(
            "http://127.0.0.1:5000/api/login",
            {
                username: $("#username-form").val(),
                password: $("#password-form").val(),
            },
            function (data, textStatus, jqXHR) {
                if (data.status_code == 0) {
                    window.location.replace("/layout"); // TODO: redirect to index
                } else {
                    if (data.status_code == 1) {
                        alert("密码错误");
                        $("#password-form").val("");
                    } else if (data.status_code == 2) {
                        alert("用户不存在");
                        $("#username-form").val("");
                        $("#password-form").val("");
                    }
                }
            },
            "json"
        );
    });
});
