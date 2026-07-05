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

    /* ---- Image carousels ---- */
    var carousels = document.querySelectorAll("[data-carousel]");
    Array.prototype.forEach.call(carousels, function (carousel) {
        var viewport = carousel.querySelector(".carousel-viewport");
        var slides = carousel.querySelectorAll(".carousel-slide");
        var prev = carousel.querySelector(".carousel-arrow--prev");
        var next = carousel.querySelector(".carousel-arrow--next");
        var dots = carousel.querySelectorAll(".carousel-dot");

        if (!viewport || slides.length <= 1) return;

        function currentIndex() {
            return Math.round(viewport.scrollLeft / viewport.clientWidth);
        }

        function goTo(index) {
            index = Math.max(0, Math.min(slides.length - 1, index));
            viewport.scrollTo({ left: index * viewport.clientWidth, behavior: "smooth" });
        }

        function update() {
            var i = currentIndex();
            Array.prototype.forEach.call(dots, function (dot, di) {
                dot.classList.toggle("is-active", di === i);
            });
            if (prev) prev.disabled = i <= 0;
            if (next) next.disabled = i >= slides.length - 1;
        }

        if (prev) prev.addEventListener("click", function () { goTo(currentIndex() - 1); });
        if (next) next.addEventListener("click", function () { goTo(currentIndex() + 1); });

        Array.prototype.forEach.call(dots, function (dot, di) {
            dot.addEventListener("click", function () { goTo(di); });
        });

        var ticking = false;
        viewport.addEventListener("scroll", function () {
            if (ticking) return;
            ticking = true;
            window.requestAnimationFrame(function () {
                update();
                ticking = false;
            });
        });
        window.addEventListener("resize", update);

        update();
    });

    /* ---- Image lightbox ---- */
    var lightbox = document.getElementById("lightbox");
    var lightboxImg = lightbox ? lightbox.querySelector(".lightbox-img") : null;
    var lightboxClose = lightbox ? lightbox.querySelector(".lightbox-close") : null;
    var lightboxPrev = lightbox ? lightbox.querySelector(".lightbox-prev") : null;
    var lightboxNext = lightbox ? lightbox.querySelector(".lightbox-next") : null;
    var lightboxCount = lightbox ? lightbox.querySelector(".lightbox-count") : null;

    var lightboxImages = [];   // [{ src, alt }, ...]
    var lightboxIndex = 0;

    function showLightboxImage(index) {
        if (!lightboxImages.length) return;
        var count = lightboxImages.length;
        lightboxIndex = ((index % count) + count) % count;   // wrap around
        var item = lightboxImages[lightboxIndex];
        lightboxImg.src = item.src;
        lightboxImg.alt = item.alt || "";

        var multi = count > 1;
        if (lightboxPrev) lightboxPrev.hidden = !multi;
        if (lightboxNext) lightboxNext.hidden = !multi;
        if (lightboxCount) {
            lightboxCount.hidden = !multi;
            lightboxCount.textContent = (lightboxIndex + 1) + " / " + count;
        }
    }

    function openLightbox(images, index) {
        if (!lightbox || !lightboxImg || !images.length) return;
        lightboxImages = images;
        showLightboxImage(index || 0);
        lightbox.classList.add("is-open");
        lightbox.setAttribute("aria-hidden", "false");
    }

    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.remove("is-open");
        lightbox.setAttribute("aria-hidden", "true");
        lightboxImg.src = "";
        lightboxImages = [];
    }

    /* Clicking a carousel / post image opens lightbox.  When the image belongs
       to a carousel, the whole image set is loaded so it can be paged through. */
    document.addEventListener("click", function (e) {
        var img = e.target.closest(".carousel-slide img, .post-hero img, .card-image img");
        if (!img) return;
        e.preventDefault();

        var carousel = img.closest("[data-carousel]");
        var images, index = 0;
        if (carousel) {
            var imgs = carousel.querySelectorAll(".carousel-slide img");
            images = Array.prototype.map.call(imgs, function (el) {
                return { src: el.src, alt: el.alt };
            });
            index = Array.prototype.indexOf.call(imgs, img);
        } else {
            images = [{ src: img.src, alt: img.alt }];
        }
        openLightbox(images, index);
    });

    if (lightboxClose) {
        lightboxClose.addEventListener("click", closeLightbox);
    }

    if (lightboxPrev) {
        lightboxPrev.addEventListener("click", function (e) {
            e.stopPropagation();
            showLightboxImage(lightboxIndex - 1);
        });
    }

    if (lightboxNext) {
        lightboxNext.addEventListener("click", function (e) {
            e.stopPropagation();
            showLightboxImage(lightboxIndex + 1);
        });
    }

    if (lightbox) {
        lightbox.addEventListener("click", function (e) {
            if (e.target === lightbox) closeLightbox();
        });
    }

    document.addEventListener("keydown", function (e) {
        if (!lightbox || !lightbox.classList.contains("is-open")) return;
        if (e.key === "Escape") {
            closeLightbox();
        } else if (e.key === "ArrowLeft") {
            showLightboxImage(lightboxIndex - 1);
        } else if (e.key === "ArrowRight") {
            showLightboxImage(lightboxIndex + 1);
        }
    });
})();
