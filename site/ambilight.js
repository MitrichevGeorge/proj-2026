function bezier(p0, p1, p2, p3, t) {
    const cX = 3 * (p1.x - p0.x);
    const bX = 3 * (p2.x - p1.x) - cX;
    const aX = p3.x - p0.x - cX - bX;

    const cY = 3 * (p1.y - p0.y);
    const bY = 3 * (p2.y - p1.y) - cY;
    const aY = p3.y - p0.y - cY - bY;

    return {
        x: aX * t * t * t + bX * t * t + cX * t + p0.x,
        y: aY * t * t * t + bY * t * t + cY * t + p0.y
    };
}

function createBezierMover(el, duration = 6000) {
    let t = 0;
    let p0 = { x: innerWidth / 2, y: innerHeight / 2 };
    let p1, p2, p3;

    function newCurve() {
        p1 = { x: Math.random() * innerWidth, y: Math.random() * innerHeight };
        p2 = { x: Math.random() * innerWidth, y: Math.random() * innerHeight };
        p3 = { x: Math.random() * innerWidth, y: Math.random() * innerHeight };
        t = 0;
    }

    newCurve();

    function animate() {
        t += 1 / (duration / 16.6); // нормализуем под 60fps

        if (t >= 1) {
            p0 = p3;
            newCurve();
        }

        const pos = bezier(p0, p1, p2, p3, t);
        el.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0)`;

        requestAnimationFrame(animate);
    }

    animate();
}

createBezierMover(document.getElementById("ambiglow-1"), 9000);
