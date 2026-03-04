# 3D Web Experience

Expert in building 3D experiences for the web -- Three.js, React Three Fiber, Spline, WebGL, and interactive 3D scenes.
Use this skill when building product configurators, 3D portfolios, immersive websites, architectural walkthroughs, or interactive 3D presentations.

Source: antigravity-awesome-skills / vibeship-spawner-skills (Apache 2.0)

## Capabilities

- Three.js implementation and React Three Fiber
- WebGL optimization and 3D model integration
- Spline workflows and 3D product configurators
- Interactive 3D scenes and scroll-driven 3D
- 3D performance optimization

## 3D Stack Selection

| Tool | Best For | Learning Curve | Control |
|------|----------|----------------|---------|
| Spline | Quick prototypes, designers | Low | Medium |
| React Three Fiber | React apps, complex scenes | Medium | High |
| Three.js vanilla | Max control, non-React | High | Maximum |
| Babylon.js | Games, heavy 3D | High | Maximum |

### Spline (Fastest Start)
```jsx
import Spline from '@splinetool/react-spline';

export default function Scene() {
  return (
    <Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
  );
}
```

### React Three Fiber
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/model.glb');
  return <primitive object={scene} />;
}

export default function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <Model />
      <OrbitControls />
    </Canvas>
  );
}
```

## 3D Model Pipeline

| Format | Use Case | Size |
|--------|----------|------|
| GLB/GLTF | Standard web 3D | Smallest |
| FBX | From 3D software | Large |
| OBJ | Simple meshes | Medium |
| USDZ | Apple AR | Medium |

### Optimization Pipeline

1. Model in Blender/etc
2. Reduce poly count (< 100K for web)
3. Bake textures (combine materials)
4. Export as GLB
5. Compress with gltf-transform
6. Test file size (< 5MB ideal)

```bash
npm install -g @gltf-transform/cli
gltf-transform optimize input.glb output.glb --compress draco --texture-compress webp
```

### Loading with Progress
```jsx
import { useGLTF, useProgress, Html } from '@react-three/drei';
import { Suspense } from 'react';

function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}%</Html>;
}

export default function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}
```

## Scroll-Driven 3D

### R3F + Scroll Controls
```jsx
import { ScrollControls, useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function RotatingModel() {
  const scroll = useScroll();
  const ref = useRef();

  useFrame(() => {
    ref.current.rotation.y = scroll.offset * Math.PI * 2;
  });

  return <mesh ref={ref}>...</mesh>;
}

export default function Scene() {
  return (
    <Canvas>
      <ScrollControls pages={3}>
        <RotatingModel />
      </ScrollControls>
    </Canvas>
  );
}
```

### GSAP + Three.js
```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.to(camera.position, {
  scrollTrigger: { trigger: '.section', scrub: true },
  z: 5,
  y: 2,
});
```

## Architectural Use Cases

### Building Walkthrough
```jsx
import { Canvas } from '@react-three/fiber';
import { PointerLockControls, useGLTF } from '@react-three/drei';

function Building() {
  const { scene } = useGLTF('/building.glb');
  return <primitive object={scene} />;
}

export default function Walkthrough() {
  return (
    <Canvas camera={{ fov: 60, position: [0, 1.7, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 10]} />
      <Building />
      <PointerLockControls />
    </Canvas>
  );
}
```

### Masterplan Viewer
```jsx
function MasterplanViewer() {
  return (
    <Canvas camera={{ position: [0, 50, 50], fov: 45 }}>
      <ambientLight intensity={0.4} />
      <directionalLight position={[20, 30, 10]} castShadow />
      <OrbitControls
        maxPolarAngle={Math.PI / 2.2}
        minDistance={10}
        maxDistance={200}
      />
      <gridHelper args={[200, 40, 0x888888, 0x444444]} />
      <Building />
    </Canvas>
  );
}
```

## Anti-Patterns

- **3D for 3D's sake**: 3D should serve a purpose. Product visualization = good. Random shapes = not.
- **Desktop-only 3D**: Most traffic is mobile. Reduce quality on mobile, provide static fallback.
- **No loading state**: 3D takes time to load. Always show progress indicator.

## Related Skills

- `threejs-fundamentals` -- Scene setup, cameras, renderers
- `threejs-materials` -- PBR materials and shaders
- `frontend-design` -- UI overlays for 3D configurators
- `canvas-design` -- 2D visual design and posters
