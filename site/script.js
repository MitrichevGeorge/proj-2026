let currentSlide = 1;
let maxSlide = 7;

const content = document.querySelector(".content");
const overlay = document.getElementById("overlay");

async function loadSlide(num) {
    const res = await fetch(`slides/${num}.html`);
    return await res.text();
}

function createSlide(html, x) {
    const slide = document.createElement("div");
    slide.className = "slide";
    slide.style.position = "absolute";
    slide.style.top = "0";
    slide.style.left = "0";
    slide.style.width = "100%";
    slide.style.height = "100%";
    slide.style.transform = `translateX(${x}%)`;
    slide.style.transition = "transform 0.6s ease";
    slide.innerHTML = html;
    return slide;
}

async function goToSlide(direction) {
    const next = currentSlide + direction;

    if (next < 1) {
        notify("Это первый слайд");
        return;
    }
    if (next > maxSlide) {
        notify("Это последний слайд");
        return;
    }

    const html = await loadSlide(next);

    const oldSlide = content.querySelector(".slide");
    const newSlide = createSlide(html, direction > 0 ? 100 : -100);

    content.appendChild(newSlide);

    requestAnimationFrame(() => {
        oldSlide.style.transform = `translateX(${direction > 0 ? -100 : 100}%)`;
        newSlide.style.transform = "translateX(0)";
    });

    setTimeout(() => oldSlide.remove(), 650);

    currentSlide = next;
}

function notify(text) {
    const n = document.createElement("div");
    n.textContent = text;
    n.style.position = "absolute";
    n.style.bottom = "40px";
    n.style.left = "50%";
    n.style.transform = "translateX(-50%)";
    n.style.padding = "10px 20px";
    n.style.background = "rgba(0,0,0,0.6)";
    n.style.borderRadius = "10px";
    n.style.color = "white";
    n.style.fontSize = "20px";
    n.style.opacity = "0";
    n.style.transition = "opacity 0.3s ease";
    n.style.zIndex = "999";

    document.body.appendChild(n);

    requestAnimationFrame(() => n.style.opacity = "1");

    setTimeout(() => {
        n.style.opacity = "0";
        setTimeout(() => n.remove(), 300);
    }, 1200);
}

(async function init() {
    const html = await loadSlide(1);
    const slide = content.querySelector(".slide");
    slide.innerHTML = html;
})();

overlay.addEventListener("click", () => goToSlide(1));

let touchStartX = 0;
let touchEndX = 0;

content.addEventListener("touchstart", e => {
    touchStartX = e.changedTouches[0].clientX;
});

content.addEventListener("touchend", e => {
    touchEndX = e.changedTouches[0].clientX;
    const dx = touchEndX - touchStartX;

    if (Math.abs(dx) < 40) return;

    if (dx < 0) goToSlide(1);
    else goToSlide(-1);
});

document.addEventListener("keydown", e => {
    if (e.key === "ArrowRight") goToSlide(1);
    if (e.key === "ArrowLeft") goToSlide(-1);
});
