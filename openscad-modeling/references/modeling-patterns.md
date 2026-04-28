# OpenSCAD Modeling Patterns

## Mental model

OpenSCAD is a declarative geometry compiler. Describe what exists, not a sequence of edits. Build durable models from parameters, reusable modules, transforms, booleans, and loops.

OpenSCAD has two major modeling styles:

1. **Constructive Solid Geometry (CSG):** combine/subtract/intersect primitive solids.
2. **2D-to-3D extrusion:** create 2D profiles with `square`, `circle`, `polygon`, `text`, imported SVG/DXF, then `linear_extrude` or `rotate_extrude`.

Preview is fast and approximate. Render/export uses exact CGAL mesh generation and is the real validation gate.

## Parameter layout

Prefer this top-of-file order:

```scad
// Units: mm
$fn_preview = 32;
$fn_final = 96;
quality = "preview"; // "preview" or "final"
$fn = quality == "final" ? $fn_final : $fn_preview;

eps = 0.01;

body_len = 90;
body_w = 36;
body_h = 18;
wall = 1.6;
clearance = 0.3;
```

Keep all magic numbers out of body geometry unless they are purely local offsets.

## Module design

Good modules are small and composable:

```scad
module rounded_box(size=[20,10,5], r=2) {
  hull() {
    for (x=[-1,1], y=[-1,1])
      translate([x*(size[0]/2-r), y*(size[1]/2-r), 0])
        cylinder(h=size[2], r=r, center=true);
  }
}

module mounting_hole(d=3, depth=10) {
  cylinder(d=d, h=depth + 2*eps, center=true);
}
```

Use descriptive module names: `wheel_arch_cutout`, `vent_slots`, `screw_boss`, `cable_channel`, `lid_snap_tab`.

## Boolean operations

### difference pattern

```scad
module bracket() {
  difference() {
    base_body();
    translate([0,0,0]) mounting_hole(d=4, depth=20);
    translate([12,0,0]) mounting_hole(d=4, depth=20);
  }
}
```

Make cutters extend beyond the body to avoid coplanar ambiguity:

```scad
cylinder(d=hole_d, h=body_h + 2*eps, center=true);
```

### union pattern

Use `union()` when additive parts overlap or when building an explicit assembly. `union()` is often optional at top level but improves readability.

### intersection clipping

Use `intersection()` to trim a complex shape to a bounding volume or make organic forms fit a known envelope.

## Repetition and radial patterns

Linear pattern:

```scad
for (i=[0:slot_count-1])
  translate([i*slot_pitch, 0, 0]) slot();
```

Centered linear pattern:

```scad
for (i=[0:n-1])
  translate([(i-(n-1)/2)*pitch, 0, 0]) slot();
```

Radial pattern:

```scad
for (a=[0:360/count:360-360/count])
  rotate([0,0,a]) translate([radius,0,0]) bolt();
```

## 2D extrusion

Use 2D first when shape is primarily a profile.

```scad
linear_extrude(height=8, center=true)
  polygon(points=[[0,12], [25,0], [0,-12], [-25,0]]);
```

Use `rotate_extrude()` for lathe-like parts:

```scad
rotate_extrude(angle=360)
  translate([10,0]) circle(r=2);
```

## Rounding and beveling

OpenSCAD has no universal fillet tool. Practical approaches:

- `hull()` between cylinders/spheres for rounded boxes and capsules.
- `minkowski()` with sphere/cylinder for rounded edges, but it can be very slow.
- Chamfer manually using polygons/extrusions or subtractive cutters.
- Fake bevels visually with thin darker/lighter bands when model is for render only.

Avoid heavy `minkowski()` in large repeated patterns unless the model is small.

## Debugging geometry

Use OpenSCAD debug modifiers in temporary work:

```scad
#cutter();   // highlight
%ghost();    // transparent background/reference
*disable();  // disable subtree
!focus();    // show only this subtree
```

Remove or comment debug modifiers before final export unless intentionally useful.

## Libraries

Use built-in/standard libraries only when they materially reduce risk. Common choices:

- MCAD library for common mechanical helpers when installed.
- BOSL/BOSL2 if already available and the project permits dependency use.

If using external libraries, document install/source requirements and avoid making a simple model depend on a heavyweight library unnecessarily.
