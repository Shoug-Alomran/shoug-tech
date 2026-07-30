(function () {
    "use strict";

    var PROJECT_ID = "xub0eqmvs9";
    var STORAGE_KEY = "shoug-analytics-consent";
    var PRIVATE_ROUTE_PREFIXES = ["/account/", "/community/"];
    var choice = null;

    try {
        choice = localStorage.getItem(STORAGE_KEY);
    } catch (error) {
        choice = null;
    }

    window.clarity = window.clarity || function () {
        (window.clarity.q = window.clarity.q || []).push(arguments);
    };

    var privateRoute = PRIVATE_ROUTE_PREFIXES.some(function (prefix) {
        return window.location.pathname.indexOf(prefix) === 0;
    });
    if (privateRoute) {
        document.documentElement.setAttribute("data-clarity-mask", "true");
    }

    // Advertising storage is intentionally never granted by this site.
    function passConsent(granted) {
        window.clarity("consentv2", {
            ad_Storage: "denied",
            analytics_Storage: granted ? "granted" : "denied"
        });
        if (!granted) {
            // Consent V2 changes the state; this legacy-compatible call also
            // clears any Clarity cookies left from an earlier accepted visit.
            window.clarity("consent", false);
        }
    }

    passConsent(choice === "granted");

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.clarity.ms/tag/" + PROJECT_ID + "?ref=bwt";
    var firstScript = document.getElementsByTagName("script")[0];
    firstScript.parentNode.insertBefore(script, firstScript);

    function isArabic() {
        var lang = String(document.documentElement.lang || "").toLowerCase();
        var saved = null;
        try {
            saved = localStorage.getItem("shoug-lang");
        } catch (error) {
            saved = null;
        }
        return lang.indexOf("ar") === 0 || saved === "ar";
    }

    function labels() {
        if (isArabic()) {
            return {
                title: "الخصوصية والتحليلات",
                body: "نستخدم Microsoft Clarity لفهم استخدام الموقع وتحسين التجربة. لن تُفعّل ملفات تعريف ارتباط التحليلات إلا بموافقتك، ولا نسمح بتخزين بيانات إعلانية.",
                accept: "السماح بالتحليلات",
                reject: "الرفض",
                settings: "خيارات الخصوصية",
                policy: "إشعار الخصوصية",
                close: "إغلاق خيارات الخصوصية"
            };
        }
        return {
            title: "Privacy & analytics",
            body: "We use Microsoft Clarity to understand site usage and improve the experience. Analytics cookies activate only with your permission, and advertising storage is never allowed.",
            accept: "Allow analytics",
            reject: "Reject",
            settings: "Privacy choices",
            policy: "Privacy notice",
            close: "Close privacy choices"
        };
    }

    function saveChoice(value) {
        try {
            localStorage.setItem(STORAGE_KEY, value);
        } catch (error) {
            // The consent signal still applies to this page if storage is blocked.
        }
        choice = value;
        passConsent(value === "granted");
        var banner = document.querySelector("[data-clarity-consent-banner]");
        if (banner) banner.hidden = true;
    }

    function showBanner() {
        var banner = document.querySelector("[data-clarity-consent-banner]");
        if (banner) banner.hidden = false;
    }

    function buildControls() {
        if (!document.body || document.querySelector("[data-clarity-consent-banner]")) return;
        var text = labels();
        var banner = document.createElement("section");
        banner.className = "shoug-consent";
        banner.setAttribute("data-clarity-consent-banner", "");
        banner.setAttribute("role", "dialog");
        banner.setAttribute("aria-live", "polite");
        banner.setAttribute("aria-labelledby", "shoug-consent-title");
        banner.hidden = choice === "granted" || choice === "denied";
        banner.innerHTML =
            '<div class="shoug-consent__copy">' +
                '<strong id="shoug-consent-title">' + text.title + '</strong>' +
                '<p>' + text.body + ' <a href="/policy/privacy-notice/">' + text.policy + '</a></p>' +
            '</div>' +
            '<div class="shoug-consent__actions">' +
                '<button type="button" data-consent-reject>' + text.reject + '</button>' +
                '<button class="shoug-consent__accept" type="button" data-consent-accept>' + text.accept + '</button>' +
            '</div>';

        var settings = document.createElement("button");
        settings.className = "shoug-consent-settings";
        settings.type = "button";
        settings.textContent = text.settings;
        settings.setAttribute("aria-label", text.settings);

        banner.querySelector("[data-consent-accept]").addEventListener("click", function () {
            saveChoice("granted");
        });
        banner.querySelector("[data-consent-reject]").addEventListener("click", function () {
            saveChoice("denied");
        });
        settings.addEventListener("click", showBanner);

        document.body.appendChild(banner);
        document.body.appendChild(settings);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", buildControls, { once: true });
    } else {
        buildControls();
    }
})();
