# Three.js Materials

Material types, PBR rendering, custom shaders, and environment maps for Three.js.
Use this skill when choosing materials, configuring PBR properties, writing custom shaders, or working with environment maps and textures.

Source: cloudai-x/threejs-skills (1.7K GitHub stars, MIT License)

## Quick Start

```javascript
import * as THREE from "three";

const material = new THREE.MeshStandardMaterial({
  color: 0x00ff00,
  roughness: 0.5,
  metalness: 0.5,
});
const mesh = new THREE.Mesh(geometry, material);
```

## Material Types Overview

| Material | Use Case | Lighting |
| --- | --- | --- |
| MeshBasicMaterial | Unlit, flat colors, wireframes | No |
| MeshLambertMaterial | Matte surfaces, performance | Yes (diffuse only) |
| MeshPhongMaterial | Shiny surfaces, specular highlights | Yes |
| MeshStandardMaterial | PBR, realistic materials | Yes (PBR) |
| MeshPhysicalMaterial | Advanced PBR, clearcoat, transmission | Yes (PBR+) |
| MeshToonMaterial | Cel-shaded, cartoon look | Yes (toon) |
| ShaderMaterial | Custom GLSL shaders | Custom |

## MeshStandardMaterial (PBR)

Recommended for realistic architectural rendering.

```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0xffffff,
  roughness: 0.5,        // 0 = mirror, 1 = diffuse
  metalness: 0.0,        // 0 = dielectric, 1 = metal
  map: colorTexture,
  roughnessMap: roughTexture,
  metalnessMap: metalTexture,
  normalMap: normalTexture,
  normalScale: new THREE.Vector2(1, 1),
  aoMap: aoTexture,       // Ambient occlusion (uses uv2!)
  aoMapIntensity: 1,
  displacementMap: dispTexture,
  displacementScale: 0.1,
  emissive: 0x000000,
  emissiveIntensity: 1,
  envMap: envTexture,
  envMapIntensity: 1,
  flatShading: false,
});

// aoMap requires second UV channel
geometry.setAttribute("uv2", geometry.attributes.uv);
```

## MeshPhysicalMaterial (Advanced PBR)

For glass, car paint, fabric, iridescent surfaces, brushed metal.

```javascript
// Glass
const glass = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  metalness: 0,
  roughness: 0,
  transmission: 1,
  thickness: 0.5,
  ior: 1.5,
  envMapIntensity: 1,
});

// Car Paint
const carPaint = new THREE.MeshPhysicalMaterial({
  color: 0xff0000,
  metalness: 0.9,
  roughness: 0.5,
  clearcoat: 1,
  clearcoatRoughness: 0.1,
});

// Fabric / Velvet
const fabric = new THREE.MeshPhysicalMaterial({
  color: 0x442244,
  sheen: 1.0,
  sheenRoughness: 0.5,
  sheenColor: new THREE.Color(0xffffff),
});
```

### MeshPhysicalMaterial Properties

```javascript
const material = new THREE.MeshPhysicalMaterial({
  // Clearcoat (car paint, lacquer)
  clearcoat: 1.0,
  clearcoatRoughness: 0.1,

  // Transmission (glass, water)
  transmission: 1.0,
  thickness: 0.5,
  attenuationDistance: 1,
  attenuationColor: new THREE.Color(0xffffff),
  ior: 1.5,

  // Sheen (fabric, velvet)
  sheen: 1.0,
  sheenRoughness: 0.5,
  sheenColor: new THREE.Color(0xffffff),

  // Iridescence (soap bubbles, oil slicks)
  iridescence: 1.0,
  iridescenceIOR: 1.3,
  iridescenceThicknessRange: [100, 400],

  // Anisotropy (brushed metal)
  anisotropy: 1.0,
  anisotropyRotation: 0,

  // Specular
  specularIntensity: 1,
  specularColor: new THREE.Color(0xffffff),
});
```

## ShaderMaterial

```javascript
const material = new THREE.ShaderMaterial({
  uniforms: {
    time: { value: 0 },
    color: { value: new THREE.Color(0xff0000) },
    texture1: { value: texture },
  },
  vertexShader: `
    varying vec2 vUv;
    uniform float time;
    void main() {
      vUv = uv;
      vec3 pos = position;
      pos.z += sin(pos.x * 10.0 + time) * 0.1;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    }
  `,
  fragmentShader: `
    varying vec2 vUv;
    uniform vec3 color;
    uniform sampler2D texture1;
    void main() {
      vec4 texColor = texture2D(texture1, vUv);
      gl_FragColor = vec4(color * texColor.rgb, 1.0);
    }
  `,
  transparent: true,
  side: THREE.DoubleSide,
});

material.uniforms.time.value = clock.getElapsedTime();
```

## Environment Maps

```javascript
// Cube texture
const cubeLoader = new THREE.CubeTextureLoader();
const envMap = cubeLoader.load(["px.jpg", "nx.jpg", "py.jpg", "ny.jpg", "pz.jpg", "nz.jpg"]);
material.envMap = envMap;

// HDR environment (recommended for architectural scenes)
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";
const rgbeLoader = new RGBELoader();
rgbeLoader.load("environment.hdr", (texture) => {
  texture.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = texture;
  scene.background = texture;
});
```

## Common Material Properties

```javascript
material.visible = true;
material.transparent = false;
material.opacity = 1.0;
material.alphaTest = 0;
material.side = THREE.FrontSide; // FrontSide, BackSide, DoubleSide
material.depthTest = true;
material.depthWrite = true;
material.blending = THREE.NormalBlending;
material.toneMapped = true;
```

## Multiple Materials

```javascript
const geometry = new THREE.BoxGeometry(1, 1, 1);
const materials = [
  new THREE.MeshBasicMaterial({ color: 0xff0000 }), // right
  new THREE.MeshBasicMaterial({ color: 0x00ff00 }), // left
  new THREE.MeshBasicMaterial({ color: 0x0000ff }), // top
  new THREE.MeshBasicMaterial({ color: 0xffff00 }), // bottom
  new THREE.MeshBasicMaterial({ color: 0xff00ff }), // front
  new THREE.MeshBasicMaterial({ color: 0x00ffff }), // back
];
const mesh = new THREE.Mesh(geometry, materials);
```

## Architectural Material Presets

```javascript
// Concrete
const concrete = new THREE.MeshStandardMaterial({
  color: 0x999999, roughness: 0.9, metalness: 0.0,
});

// Wood
const wood = new THREE.MeshStandardMaterial({
  color: 0x8B6914, roughness: 0.7, metalness: 0.0,
});

// Steel
const steel = new THREE.MeshStandardMaterial({
  color: 0xC0C0C0, roughness: 0.3, metalness: 1.0,
});

// Brick
const brick = new THREE.MeshStandardMaterial({
  color: 0xA0522D, roughness: 0.85, metalness: 0.0,
});
```

## Performance Tips

1. Simpler materials are faster: Basic < Lambert < Phong < Standard < Physical
2. Use `alphaTest` instead of `transparency` when possible
3. Reuse materials -- same material instance = batched draw calls
4. Limit active lights -- each light adds shader complexity
5. Always `dispose()` materials when done

```javascript
const materialCache = new Map();
function getMaterial(color) {
  const key = color.toString(16);
  if (!materialCache.has(key)) {
    materialCache.set(key, new THREE.MeshStandardMaterial({ color }));
  }
  return materialCache.get(key);
}
```

## See Also

- `threejs-fundamentals` -- Scene setup and core classes
- `3d-web-experience` -- Full 3D web architecture patterns
