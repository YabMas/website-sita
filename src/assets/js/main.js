/* ==========================================================================
   L'artisane sauvage — main.js
   Mobile nav toggle + image lightbox
   ========================================================================== */

(function () {
    "use strict";

    /* ---- Mobile nav toggle ---- */
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");

    if (toggle && nav) {
        toggle.addEventListener("click", function () {
            var expanded = toggle.getAttribute("aria-expanded") === "true";
            toggle.setAttribute("aria-expanded", String(!expanded));
            toggle.classList.toggle("is-active");
            nav.classList.toggle("is-open");
        });
    }

    /* ---- Image lightbox ---- */
    var lightbox = document.getElementById("lightbox");
    var lightboxImg = lightbox ? lightbox.querySelector(".lightbox-img") : null;
    var lightboxClose = lightbox ? lightbox.querySelector(".lightbox-close") : null;

    function openLightbox(src, alt) {
        if (!lightbox || !lightboxImg) return;
        lightboxImg.src = src;
        lightboxImg.alt = alt || "";
        lightbox.classList.add("is-open");
        lightbox.setAttribute("aria-hidden", "false");
    }

    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.remove("is-open");
        lightbox.setAttribute("aria-hidden", "true");
        lightboxImg.src = "";
    }

    /* Clicking showcase / post images opens lightbox */
    document.addEventListener("click", function (e) {
        var img = e.target.closest(".showcase-img, .post-hero img, .card-image img");
        if (img) {
            e.preventDefault();
            openLightbox(img.src, img.alt);
        }
    });

    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    if (lightbox) {
        lightbox.addEventListener("click", function (e) {
            if (e.target === lightbox) closeLightbox();
        });
    }

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeLightbox();
    });
})();
