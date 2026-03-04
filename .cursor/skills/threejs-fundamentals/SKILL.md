# Three.js Fundamentals

Three.js scene setup, cameras, renderer, Object3D hierarchy, and coordinate systems.
Use this skill when setting up 3D scenes, creating cameras, configuring renderers, managing object hierarchies, or working with transforms.

Source: cloudai-x/threejs-skills (1.7K GitHub stars, MIT License)

## Quick Start

```javascript
import * as THREE from "three";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000,
);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const dirLight = new THREE.DirectionalLight(0xffffff, 1);
dirLight.position.set(5, 5, 5);
scene.add(dirLight);

camera.position.z = 5;

function animate() {
  requestAnimationFrame(animate);
  cube.rotation.x += 0.01;
  cube.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## Core Classes

### Scene

```javascript
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);
scene.background = texture;           // Skybox texture
scene.background = cubeTexture;       // Cubemap
scene.environment = envMap;           // Environment map for PBR
scene.fog = new THREE.Fog(0xffffff, 1, 100);       // Linear fog
scene.fog = new THREE.FogExp2(0xffffff, 0.02);     // Exponential fog
```

### Cameras

```javascript
// PerspectiveCamera(fov, aspect, near, far)
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10);
camera.lookAt(0, 0, 0);
camera.updateProjectionMatrix();

// OrthographicCamera - no perspective distortion, good for 2D/isometric
const aspect = window.innerWidth / window.innerHeight;
const frustumSize = 10;
const orthoCamera = new THREE.OrthographicCamera(
  (frustumSize * aspect) / -2, (frustumSize * aspect) / 2,
  frustumSize / 2, frustumSize / -2, 0.1, 1000,
);

// CubeCamera - environment maps for reflections
const cubeRenderTarget = new THREE.WebGLCubeRenderTarget(256);
const cubeCamera = new THREE.CubeCamera(0.1, 1000, cubeRenderTarget);
```

### WebGLRenderer

```javascript
const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector("#canvas"),
  antialias: true,
  alpha: true,
  powerPreference: "high-performance",
  preserveDrawingBuffer: true,
});

renderer.setSize(width, height);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
```

### Object3D

```javascript
const obj = new THREE.Object3D();

// Transform
obj.position.set(x, y, z);
obj.rotation.set(x, y, z);
obj.quaternion.set(x, y, z, w);
obj.scale.set(x, y, z);

// World transforms
obj.getWorldPosition(targetVector);
obj.getWorldQuaternion(targetQuaternion);
obj.getWorldDirection(targetVector);

// Hierarchy
obj.add(child);
obj.remove(child);
obj.traverse((child) => {
  if (child.isMesh) child.material.color.set(0xff0000);
});
```

### Group & Mesh

```javascript
const group = new THREE.Group();
group.add(mesh1);
group.add(mesh2);
scene.add(group);

const mesh = new THREE.Mesh(geometry, material);
mesh.castShadow = true;
mesh.receiveShadow = true;
mesh.frustumCulled = true;
```

## Coordinate System

Right-handed: +Z toward viewer, +Y up, +X right.

```javascript
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper); // Red=X, Green=Y, Blue=Z
```

## Math Utilities

```javascript
// Vector3
const v = new THREE.Vector3(x, y, z);
v.add(v2); v.sub(v2); v.normalize(); v.lerp(target, alpha);
v.length(); v.distanceTo(v2); v.dot(v2); v.cross(v2);
v.project(camera); v.unproject(camera);

// Color
const color = new THREE.Color(0xff0000);
color.lerp(otherColor, alpha);

// MathUtils
THREE.MathUtils.clamp(value, min, max);
THREE.MathUtils.lerp(start, end, alpha);
THREE.MathUtils.degToRad(degrees);
THREE.MathUtils.radToDeg(radians);
```

## Common Patterns

### Cleanup
```javascript
function dispose() {
  mesh.geometry.dispose();
  if (Array.isArray(mesh.material)) {
    mesh.material.forEach((m) => m.dispose());
  } else {
    mesh.material.dispose();
  }
  texture.dispose();
  scene.remove(mesh);
  renderer.dispose();
}
```

### Clock for Animation
```javascript
const clock = new THREE.Clock();
function animate() {
  const delta = clock.getDelta();
  mesh.rotation.y += delta * 0.5;
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
```

### Loading Manager
```javascript
const manager = new THREE.LoadingManager();
manager.onLoad = () => console.log("All loaded");
manager.onProgress = (url, loaded, total) => console.log(`${loaded}/${total}`);
const textureLoader = new THREE.TextureLoader(manager);
```

## Performance Tips

1. Cache `getWorldPosition` results -- avoid calling in loops
2. Object pooling -- reuse objects instead of creating/destroying
3. Use `THREE.LOD` for distance-based mesh switching
4. Merge static geometries with `mergeGeometries()`
5. Use instancing for repeated objects
6. Limit draw calls: atlas textures, shared materials

```javascript
// LOD
const lod = new THREE.LOD();
lod.addLevel(highDetailMesh, 0);
lod.addLevel(medDetailMesh, 50);
lod.addLevel(lowDetailMesh, 100);
scene.add(lod);
```

## See Also

- `threejs-materials` -- Material types and properties
- `threejs-lighting` -- Light types and shadows
- `3d-web-experience` -- Full 3D web architecture patterns
