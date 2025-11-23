"use client";

import { useEffect } from "react";

export default function Particles() {
    useEffect(() => {
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js";
        script.async = true;
        script.onload = () => {
            (window as any).particlesJS("particles-js", {
                particles: {
                    number: { value: 100, density: { enable: true, value_area: 800 } },
                    color: { value: ["#135389", "#FEFBFF"] },
                    shape: { type: ["circle"] },
                    opacity: { value: 0.8, random: true },
                    size: { value: 6, random: true },
                    move: { enable: true, speed: 4, out_mode: "bounce" },
                    line_linked: { enable: true, distance: 140, color: "#FEFBFF", opacity: 0.5, width: 1 },
                },
                interactivity: {
                    detect_on: "canvas",
                    events: { onhover: { enable: true, mode: "bubble" }, onclick: { enable: true, mode: "push" }, resize: true },
                    modes: { bubble: { distance: 200, size: 9 }, push: { particles_nb: 8 } },
                },
                retina_detect: true,
            });
        };
        document.body.appendChild(script);
    }, []);

    return <div id="particles-js" className="particles-bg" />;
}
