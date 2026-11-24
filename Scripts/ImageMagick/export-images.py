#!/usr/bin/env python3
"""Export images from one folder to a new folder using ImageMagick 7.

Run python3 export-images.py --help for profiles and options. Install magick
on PATH. Inputs are left in place. The output folder must not already exist.
"""
import argparse
from pathlib import Path
import shutil
import subprocess


FORMATS = {".cr2", ".cr3", ".dng", ".jpeg", ".jpg", ".png", ".psd",
           ".svg", ".tif", ".tiff", ".webp"}
STUDIO = (
    ("high-jpg", "jpg", "4600", False, None),
    ("high-png", "png", "4600", False, None),
    ("high-webp", "webp", "2000", False, 100),
    ("low-jpg", "jpg", "1600", False, None),
    ("low-png", "png", "1600", False, None),
    ("low-webp", "webp", "800", False, 100),
    ("web-jpg", "jpg", "500", True, None),
    ("web-png", "png", "500", True, None),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("profile", choices=("studio", "jpeg", "datasheet", "svg"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--max-size", type=int, help="maximum edge in pixels for jpeg")
    parser.add_argument("--strip-metadata", action="store_true")
    args = parser.parse_args()
    if shutil.which("magick") is None:
        parser.error("ImageMagick 7 (magick) was not found on PATH")
    if not args.input.is_dir():
        parser.error("input must be an existing directory")
    if args.max_size is not None and (args.profile != "jpeg" or args.max_size < 1):
        parser.error("--max-size requires the jpeg profile and a positive value")
    extensions = {"datasheet": {".psd"}, "svg": {".svg"}}.get(args.profile, FORMATS)
    inputs = sorted(p for p in args.input.iterdir() if p.is_file() and p.suffix.lower() in extensions)
    if not inputs:
        parser.error("no supported images found")
    stems = {p.stem.casefold() for p in inputs}
    if len(stems) != len(inputs):
        parser.error("input files have conflicting basenames")
    try:
        args.output.mkdir()
    except OSError as error:
        parser.error(str(error))

    profiles = {
        "studio": STUDIO,
        "jpeg": (("", "jpg", str(args.max_size) if args.max_size else None, False, None),),
        "datasheet": (("", "png", "1200", False, None),),
        "svg": (("", "png", None, False, None),),
    }
    for folder, extension, size, square, quality in profiles[args.profile]:
        destination = args.output / folder
        destination.mkdir(exist_ok=True)
        for source in inputs:
            # The first frame/layer is the composite for typical layered PSD inputs.
            cmd = ["magick", f"{source.resolve()}[0]", "-auto-orient"]
            if args.profile == "datasheet":
                cmd += ["-trim", "+repage"]
            if size:
                cmd += ["-resize", f"{size}x{size}>"]
            background = "white" if extension == "jpg" else "none"
            if extension == "jpg":
                cmd += ["-background", background, "-alpha", "remove", "-alpha", "off"]
            if square:
                cmd += ["-background", background, "-gravity", "Center", "-extent", f"{size}x{size}"]
            if quality is not None:
                cmd += ["-quality", str(quality)]
            if args.strip_metadata:
                cmd += ["-strip"]
            cmd.append(str((destination / f"{source.stem}.{extension}").resolve()))
            status = subprocess.call(cmd)
            if status:
                return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
