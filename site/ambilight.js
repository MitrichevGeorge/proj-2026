function createInfinityMover(el) {
    const centerX = innerWidth / 2;
    const centerY = innerHeight / 2;

    let t = Math.random() * Math.PI * 2;

    // случайная амплитуда и скорость
    let amp = 150 + Math.random() * 120;
    let speed = 0.005 + Math.random() * 0.004;

    // лёгкое смещение центра
    let offsetX = (Math.random() - 0.5) * 120;
    let offsetY = (Math.random() - 0.5) * 80;

    function animate() {
        t += speed;

        // формула горизонтальной восьмёрки
        const denom = 1 + Math.sin(t) ** 2;

        const x = amp * Math.cos(t) / denom;
        const y = amp * Math.sin(t) * Math.cos(t) / denom;
        console.log(x, y);

        el.style.transform =
            `translate3d(${centerX + x + offsetX}px, ${centerY + y + offsetY}px, 0)`;

        requestAnimationFrame(animate);
    }

    animate();
}

createInfinityMover(document.getElementById("ambiglow-1"));