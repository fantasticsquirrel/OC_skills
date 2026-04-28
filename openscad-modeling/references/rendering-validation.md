# OpenSCAD Rendering and Validation

## Required checks by task type

### Visual concept/model

Run at least:

```bash
xvfb-run -a openscad -o /tmp/model.png --imgsize=1600,1100 --camera=0,0,0,60,0,35,180 model.scad
identify /tmp/model.png
```

Copy important PNGs to an allowed workspace path before using image analysis or sending them.

### Printable model

Run at least:

```bash
openscad -o /tmp/model.stl model.scad
ls -lh /tmp/model.stl
```

If `openscad` needs a display even for PNG, use `xvfb-run -a`. STL/3MF exports often work without Xvfb but may vary by install.

### Skill/example validation

Run both PNG and STL/3MF on a small test model so syntax and CGAL paths are verified.

## Useful CLI forms

PNG:

```bash
openscad -o out.png --imgsize=1200,900 --camera=0,0,0,55,0,35,160 model.scad
```

Headless PNG:

```bash
xvfb-run -a openscad -o out.png --imgsize=1200,900 --camera=0,0,0,55,0,35,160 model.scad
```

STL:

```bash
openscad -o out.stl model.scad
```

3MF:

```bash
openscad -o out.3mf model.scad
```

SVG from 2D/projection:

```bash
openscad -o out.svg model.scad
```

## Camera notes

OpenSCAD `--camera` supports view parameters. A practical form is:

```text
--camera=translateX,translateY,translateZ,rotX,rotY,rotZ,distance
```

Useful starting angles:

- Hero/isometric: `--camera=0,0,0,60,0,35,180`
- Front: `--camera=0,0,0,90,0,0,180`
- Side: `--camera=0,0,0,90,0,90,180`
- Top: `--camera=0,0,0,0,0,0,180`
- Rear high: `--camera=0,0,0,65,0,215,180`

Adjust camera distance to fit the model. If output is blank, increase distance or verify the model is near origin.

## Render artifact workflow

Use predictable paths:

```bash
mkdir -p /tmp/openscad-renders/<project>
xvfb-run -a openscad -o /tmp/openscad-renders/<project>/hero.png ... model.scad
mkdir -p /root/.openclaw/workspace/artifacts/<project>
cp /tmp/openscad-renders/<project>/*.png /root/.openclaw/workspace/artifacts/<project>/
```

Why copy to workspace/artifacts: tools that analyze or deliver images may reject arbitrary `/tmp` paths.

## Interpreting errors

- `Parser error`: syntax issue; check semicolons/braces/commas.
- `Can't open include file`: dependency missing or include path wrong.
- `Object isn't a valid 2-manifold`: non-printable or self-intersecting geometry; inspect booleans and coplanar faces.
- `Current top level object is empty`: model subtracted away, hidden by condition, or top-level module not called.
- Long render times: reduce `$fn`, simplify `minkowski`, render submodules, or add a `quality` parameter.

## Multi-angle review

For visual work, render 2–4 angles:

```bash
for view in hero side top rear; do
  # choose camera per view
  xvfb-run -a openscad -o "$out/$view.png" --imgsize=1600,1100 --camera="$camera" model.scad
done
```

Then inspect the images. Do not assume a successful render looks good.
