#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: render-openscad.sh <model.scad> [--png] [--stl] [--3mf] [--outdir DIR] [--imgsize WIDTH,HEIGHT] [--camera CAMERA]

Examples:
  render-openscad.sh model.scad --png --stl --outdir /tmp/openscad-renders
  render-openscad.sh model.scad --png --imgsize 1600,1100 --camera 0,0,0,60,0,35,180
USAGE
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi
model="$1"; shift
if [[ ! -f "$model" ]]; then echo "Model not found: $model" >&2; exit 2; fi

want_png=false
want_stl=false
want_3mf=false
outdir="/tmp/openscad-renders"
imgsize="1600,1100"
camera="0,0,0,60,0,35,180"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --png) want_png=true; shift ;;
    --stl) want_stl=true; shift ;;
    --3mf) want_3mf=true; shift ;;
    --outdir) outdir="$2"; shift 2 ;;
    --imgsize) imgsize="$2"; shift 2 ;;
    --camera) camera="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if ! $want_png && ! $want_stl && ! $want_3mf; then
  want_png=true
fi

mkdir -p "$outdir"
base="$(basename "$model" .scad)"

run_openscad_png() {
  local out="$1"
  if command -v xvfb-run >/dev/null 2>&1; then
    xvfb-run -a openscad -o "$out" --imgsize="$imgsize" --camera="$camera" "$model"
  else
    openscad -o "$out" --imgsize="$imgsize" --camera="$camera" "$model"
  fi
}

if $want_png; then
  out="$outdir/${base}.png"
  run_openscad_png "$out"
  echo "$out"
fi

if $want_stl; then
  out="$outdir/${base}.stl"
  openscad -o "$out" "$model"
  echo "$out"
fi

if $want_3mf; then
  out="$outdir/${base}.3mf"
  openscad -o "$out" "$model"
  echo "$out"
fi
