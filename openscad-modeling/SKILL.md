---
name: openscad-modeling
description: Create, improve, debug, render, and validate OpenSCAD parametric CAD models. Use when working with .scad files, CSG modeling, 2D-to-3D extrusion, printable mechanical parts, procedural/parametric geometry, OpenSCAD CLI rendering, STL/3MF/PNG export, or visual QA of generated OpenSCAD models.
---

# OpenSCAD Modeling

Use this skill to turn a design request into a clean, parameterized `.scad` model and verify it with OpenSCAD renders/exports. OpenSCAD is code-first CAD: prioritize explicit geometry, parameters, modules, and reproducible command-line validation over hand-wavy artistic modeling.

## Core workflow

1. **Clarify the object and output target**
   - Determine whether the goal is: printable part, visual concept, diagram, toy/model, fixture, enclosure, cable/coil/helix, or library component.
   - Ask only for dimensions/tolerances that materially affect the model. If unspecified, choose reasonable defaults and put them in top-level parameters.
   - Decide output proof: PNG preview for visual work; STL/3MF for printable geometry; both for anything intended to manufacture.

2. **Structure the model before writing details**
   - Put user-tunable values at top: dimensions, clearances, wall thickness, `$fn`, rendering/detail mode.
   - Split into named `module`s for parts/subassemblies.
   - Keep transforms local and readable: `translate`, `rotate`, `scale` close to the primitive/module they affect.
   - Use `difference()` for subtractive cuts, `union()` for additive assemblies, `intersection()` for clipping.

3. **Model in stable passes**
   - Start with blockout primitives (`cube`, `cylinder`, `sphere`).
   - Add booleans and repeated features.
   - Add bevels/rounding/fillets only after proportions are right.
   - Add detail layers last (vents, bolts, grooves, panel seams, labels, decorative ribs).

4. **Validate early and often**
   - Run syntax/render checks with the OpenSCAD CLI.
   - Render at least one PNG preview when visual quality matters.
   - Export STL/3MF when printability matters.
   - Inspect warnings for non-manifold geometry, invalid polygons, missing includes, or CGAL errors.

5. **Iterate from evidence**
   - If proportions are wrong, fix primary parameters first.
   - If the object is visually flat, add silhouette changes, bevels, seams, layered details, and camera angles.
   - If render/export fails, simplify to isolate the bad module or boolean.

## When to load references

- For design patterns, parameterization, CSG, modules, loops, extrusion, and printability: read `references/modeling-patterns.md`.
- For command-line rendering, screenshots, export formats, cameras, and validation: read `references/rendering-validation.md`.
- For style recipes like vehicles, cables/helices, enclosures, mechanical parts, and decorative surface detail: read `references/shape-recipes.md`.

## OpenSCAD language essentials

Use these primitives and constructs first:

```scad
// quality/detail
$fn = 64;

// primitives
cube([x, y, z], center=true);
cylinder(h=h, r=r, center=true);
cylinder(h=h, d=d, center=true);
sphere(r=r);

// transforms
translate([x, y, z]) child();
rotate([rx, ry, rz]) child();
scale([sx, sy, sz]) child();

// booleans
union() { ... }
difference() { base(); cutter(); }
intersection() { ... }

// reusable code
module part(width=10) { ... }
function f(x) = x * 2;

// repetition
for (i = [0:n-1]) { ... }
```

Remember: OpenSCAD variables are assignment-like but behave functionally; later mutation does not work like imperative programming. Prefer explicit parameters and functions.

## Good model conventions

- Use millimeters unless the user states otherwise.
- Name dimensions semantically: `body_len`, `wall`, `axle_d`, `clearance`, not `x1` and `foo`.
- Add comments for non-obvious geometry and every major module.
- Prefer `center=true` for symmetric parts; document coordinate origin.
- Use `eps = 0.01` or similar for boolean cutters that must pass fully through a body.
- Use `$fn` deliberately: low for test renders, higher for final curves.
- Keep final top-level call simple: `model();` or `assembly();`.

## Printability guardrails

For printable parts:

- Wall thickness: usually >= 1.2 mm for FDM unless otherwise specified.
- Clearances: 0.2–0.4 mm for sliding/tight FDM fits; larger if printer is unknown.
- Avoid infinitely thin surfaces: all features need thickness.
- Avoid unsupported horizontal spans unless intended for supports/bridging.
- Export exact geometry with Render/CGAL, not preview-only OpenCSG.
- Prefer STL/3MF export after a successful render.

## CLI validation quick start

Use the bundled helper when available:

```bash
bash skills/openscad-modeling/scripts/render-openscad.sh path/to/model.scad --png --stl --outdir /tmp/openscad-renders
```

Direct commands:

```bash
# PNG preview, headless when needed
xvfb-run -a openscad -o /tmp/model.png --imgsize=1600,1100 --camera=0,0,0,60,0,35,180 path/to/model.scad

# STL export / CGAL validation
openscad -o /tmp/model.stl path/to/model.scad
```

Store user-facing render artifacts under the workspace or another allowed media path, not only `/tmp`, if they need to be analyzed or sent.

## Common failure modes

- **Blank render:** camera too far/near, model outside view, hidden by boolean subtraction, zero dimensions.
- **OpenSCAD syntax error:** missing semicolon, missing brace, invalid vector/list, wrong module call.
- **CGAL failure:** non-manifold geometry, coplanar surfaces, invalid polygon winding, zero-thickness intersections.
- **Boolean artifacts:** cutters barely touch surfaces; make cutters extend past the target by `eps`.
- **Slow renders:** too much `$fn`, heavy `minkowski`, nested hulls, repeated high-resolution curved cuts.
- **Looks primitive:** add silhouette variation, bevels/fillets, layered surface panels, seams, grooves, repeated fasteners, and better camera/lighting.

## Output expectations

When completing OpenSCAD work, report:

- Files created/edited.
- Validation command(s) run and result.
- Render/export artifact paths.
- Any known limitations or next refinements.

For visual work, include at least one preview path. For printable work, include an exported STL/3MF path or explain why export was not possible.
