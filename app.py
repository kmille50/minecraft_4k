import streamlit as st
import streamlit.components.v1 as components

st.title("🧱 Mini Minecraft 3D")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; }
    canvas { display: block; }
  </style>
</head>
<body>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>
let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);

let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Lumière
let light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 5);
scene.add(light);

// Sol en cubes (style Minecraft)
let size = 10;

for (let x = 0; x < size; x++) {
  for (let z = 0; z < size; z++) {
    let geometry = new THREE.BoxGeometry(1, 1, 1);
    let material = new THREE.MeshLambertMaterial({ color: 0x55aa55 });
    let cube = new THREE.Mesh(geometry, material);

    cube.position.set(x, 0, z);
    scene.add(cube);
  }
}

// Joueur (cube bleu)
let playerGeo = new THREE.BoxGeometry(0.8, 0.8, 0.8);
let playerMat = new THREE.MeshLambertMaterial({ color: 0x0000ff });
let player = new THREE.Mesh(playerGeo, playerMat);
player.position.set(5, 1, 5);
scene.add(player);

// Caméra
camera.position.set(5, 5, 10);

// Contrôles clavier
document.addEventListener("keydown", (event) => {
  let step = 0.2;

  if (event.key === "ArrowUp") player.position.z -= step;
  if (event.key === "ArrowDown") player.position.z += step;
  if (event.key === "ArrowLeft") player.position.x -= step;
  if (event.key === "ArrowRight") player.position.x += step;
});

// Animation
function animate() {
  requestAnimationFrame(animate);

  // Caméra suit le joueur
  camera.position.x = player.position.x;
  camera.position.z = player.position.z + 5;
  camera.lookAt(player.position);

  renderer.render(scene, camera);
}

animate();
</script>

</body>
</html>
"""

components.html(html_code, height=600)