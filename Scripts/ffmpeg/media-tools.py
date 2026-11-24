#!/usr/bin/env python3
"""Convert, inspect or split one media file using FFmpeg and FFprobe.

Run python3 media-tools.py --help for commands, or add --help after a command.
Install FFmpeg (with libx264 for video commands) and put it on PATH.
Each conversion takes an explicit output path and refuses to overwrite files.
"""
import argparse
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("mp3", "Convert an audio track to 128 kbps MP3"),
        ("proxy", "Create a 720p-or-smaller H.264 MP4 viewing copy"),
        ("h264", "Encode a high-quality H.264 MOV with AAC audio"),
        ("watermark", "Overlay a supplied PNG at the top left of a video"),
        ("duration", "Print the duration reported by FFprobe, in seconds"),
        ("split", "Split at keyframes into numbered files in a new directory"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("input", type=Path)
        if name != "duration":
            command.add_argument("output", type=Path)
        if name == "watermark":
            command.add_argument("overlay", type=Path, help="PNG overlay")
        if name == "split":
            command.add_argument("--seconds", type=int, default=30)
    args = parser.parse_args()
    if not args.input.is_file():
        parser.error("input must be an existing file")
    source = str(args.input.resolve())
    tool = "ffprobe" if args.command == "duration" else "ffmpeg"
    if shutil.which(tool) is None:
        parser.error(f"{tool} was not found on PATH")
    if args.command == "duration":
        return subprocess.call([tool, "-v", "error", "-show_entries", "format=duration",
                                "-of", "default=noprint_wrappers=1:nokey=1", source])

    output = args.output.resolve()
    if output.exists():
        parser.error("output already exists")
    if not output.parent.is_dir():
        parser.error("output parent directory must exist")
    base = [tool, "-nostdin", "-n", "-i", source]
    video = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac"]
    requirements = {"mp3": ".mp3", "proxy": ".mp4", "h264": ".mov", "watermark": ".mp4"}
    if args.command in requirements and output.suffix.lower() != requirements[args.command]:
        parser.error(f"output must end in {requirements[args.command]}")
    if args.command == "mp3":
        options = ["-vn", "-ar", "44100", "-ac", "2", "-b:a", "128k"]
    elif args.command == "proxy":
        options = ["-vf", "scale=-2:min(720\\,trunc(ih/2)*2)", *video, "-crf", "27"]
    elif args.command == "h264":
        options = [*video, "-crf", "4", "-preset", "slow"]
    elif args.command == "watermark":
        if not args.overlay.is_file() or args.overlay.suffix.lower() != ".png":
            parser.error("overlay must be an existing PNG")
        options = ["-i", str(args.overlay.resolve()), "-filter_complex", "[0:v][1:v]overlay=0:0[v]",
                   "-map", "[v]", "-map", "0:a?", *video]
    else:
        if args.seconds < 1:
            parser.error("--seconds must be positive")
        if args.input.suffix.lower() not in {".mov", ".mp4", ".mkv"}:
            parser.error("split supports MOV, MP4 and MKV inputs")
        try:
            output.mkdir()
        except OSError as error:
            parser.error(str(error))
        options = ["-map", "0", "-c", "copy", "-f", "segment", "-segment_time",
                   str(args.seconds), "-reset_timestamps", "1"]
        output = output / f"segment-%03d{args.input.suffix.lower()}"
    return subprocess.call([*base, *options, str(output)])


if __name__ == "__main__":
    raise SystemExit(main())
