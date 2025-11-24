// Set current year in footer
document.addEventListener("DOMContentLoaded", () => {
  const yearSpan = document.getElementById("year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
});

// FAQ Accordion
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".faq-question");
  if (!btn) return;

  const item = btn.closest(".faq-item");
  const answer = item.querySelector(".faq-answer");

  const isOpen = item.classList.contains("open");
  document.querySelectorAll(".faq-item").forEach((it) => {
    it.classList.remove("open");
    const ans = it.querySelector(".faq-answer");
    if (ans) ans.style.maxHeight = null;
  });

  if (!isOpen) {
    item.classList.add("open");
    answer.style.maxHeight = answer.scrollHeight + "px";
  }
});

// Smooth scroll for in-page anchors
document.addEventListener("click", (e) => {
  const link = e.target.closest('a[href^="#"]');
  if (!link) return;

  const targetId = link.getAttribute("href").slice(1);
  const target = document.getElementById(targetId);
  if (target) {
    e.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

/* Three.js Animated Heart
   - Simple glowing, slowly rotating heart-ish torus shape
   - Only runs on pages that include #heartCanvas and THREE is loaded
*/
(function initHeartScene() {
  const canvas = document.getElementById("heartCanvas");
  if (!canvas || typeof THREE === "undefined") return;

  const scene = new THREE.Scene();
  scene.background = null;

  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true
  });

  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(0, 0, 4);

  const geometry = new THREE.TorusKnotGeometry(0.9, 0.28, 220, 32);
  const material = new THREE.MeshPhongMaterial({
    color: 0xe53935,
    emissive: 0xff5252,
    emissiveIntensity: 0.4,
    shininess: 90,
    specular: 0xffffff
  });
  const heartMesh = new THREE.Mesh(geometry, material);
  scene.add(heartMesh);

  const ambient = new THREE.AmbientLight(0xffffff, 0.3);
  scene.add(ambient);

  const pointLight1 = new THREE.PointLight(0xff6666, 1.6, 20);
  pointLight1.position.set(3, 2, 4);
  scene.add(pointLight1);

  const pointLight2 = new THREE.PointLight(0xffffff, 0.9, 20);
  pointLight2.position.set(-3, -2, -4);
  scene.add(pointLight2);

  function onResize() {
    const width = canvas.clientWidth || canvas.offsetWidth || 400;
    const height = canvas.clientHeight || 260;
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
  }

  window.addEventListener("resize", onResize);
  onResize();

  let t = 0;
  function animate() {
    requestAnimationFrame(animate);
    t += 0.02;
    heartMesh.rotation.y += 0.01;
    heartMesh.rotation.x = Math.sin(t * 0.5) * 0.3;
    heartMesh.scale.setScalar(1 + Math.sin(t) * 0.06);
    renderer.render(scene, camera);
  }

  animate();
})();

/*
 THREE.JS PROMPT (as requested)
 You can copy-paste this text into an AI code assistant if you want a more
 advanced animated heart using Three.js:

 "Create a modern Three.js hero background for a medical website in a red and
 black theme. The scene should show a glowing red 3D heart shape (not cartoonish)
 floating in the center, slowly rotating and pulsing in size like a heartbeat.
 Use soft point lights in red and white to highlight the edges, with a subtle
 dark gradient background and faint particles drifting around the heart. The
 animation must be smooth, responsive to canvas size, and optimized for fast
 loading on typical laptops and mobile devices."
*/
