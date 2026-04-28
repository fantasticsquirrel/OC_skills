# OpenSCAD Shape Recipes

## Vehicles and stylized objects

Start with silhouette first:

1. Main body wedge/rounded box.
2. Cabin/cockpit as a smaller raised volume.
3. Wheel wells/cutouts using subtractive cylinders or arches.
4. Wheels as cylinders rotated 90 degrees.
5. Spoilers, diffusers, vents, side intakes, seams, headlights.
6. Color blocks with `%`/`color()` for preview PNGs.

Useful modules:

- `rounded_box(size, r)` using `hull()` of corner cylinders.
- `wheel(d, w)` as a rotated cylinder plus tire/rim layers.
- `vent_slots(count, pitch)` as repeated subtractive narrow cubes.
- `panel_seam()` as thin dark inset grooves.

For “sexy” visual output, flat primitives are not enough. Add rake, stance, wheel size, layered surface detail, thin seams, and distinct front/rear/side features.

## Cables, coils, and helices

OpenSCAD has no native sweep-along-path. Use one of these:

1. Approximate a cable by chaining short cylinders/spheres between sampled points.
2. Use `polyhedron()` for advanced tube meshes.
3. Generate path points externally if the geometry is complex.

For helix point sampling:

```scad
function helix_point(t, r=10, pitch=4) = [r*cos(t), r*sin(t), pitch*t/360];
```

Approximate tube segments with small cylinders oriented between points; for high quality, prefer a mesh generator script outside OpenSCAD.

## Enclosures and boxes

Pattern:

1. Outer rounded box.
2. Subtract inner cavity using `wall` and `eps`.
3. Add lid lip/rabbet.
4. Add screw bosses and holes.
5. Add vents/ports/cable pass-through.
6. Add labels or alignment marks.

Guardrails:

- `wall >= 1.2` for FDM.
- Boss outer diameter usually screw diameter + 3–5 mm.
- Add clearances around lids and ports.

## Brackets and fixtures

Pattern:

1. Base plate.
2. Upright/support geometry.
3. Fillets/chamfers or triangular gussets.
4. Mounting holes.
5. Optional countersinks/counterbores.

Triangular gusset example:

```scad
module gusset(thick=4, h=20, w=20) {
  rotate([90,0,0])
    linear_extrude(height=thick, center=true)
      polygon([[0,0],[w,0],[0,h]]);
}
```

## Text and labels

```scad
linear_extrude(height=0.8)
  text("LABEL", size=6, halign="center", valign="center");
```

For embossed text, add it. For engraved text, subtract it with a slightly deeper extrusion.

## Surface detail without wrecking printability

- Use shallow grooves instead of tiny raised wires when printing small.
- Keep decorative cuts wider than nozzle diameter if printable.
- Put cosmetic high-detail features behind a parameter: `show_detail = true;`.
- Use `quality` to choose lower `$fn` during iteration.
