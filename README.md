# Scerno Scripts Toolbox

Standalone utilities from earlier Scerno workflows. Each script documents its dependencies and how to run it.

| Script | Purpose |
| --- | --- |
| [123-reg zonefile creation](Scripts/DNS/123-reg-zonefile-creation.js) | Export the DNS records shown on a legacy 123-reg page. [Instructions and upstream terms](Scripts/DNS/README.md) |
| [FFmpeg media tools](Scripts/ffmpeg/media-tools.py) | MP3 conversion, video proxies, H.264 MOV, watermarking, duration and splitting |
| [ImageMagick image exports](Scripts/ImageMagick/export-images.py) | Studio image sets, JPEG conversion, trimmed datasheet PNGs and SVG rasterisation |

## Examples

Run the Python scripts with Python 3 and the command-line tools listed above on your PATH. Paths in the examples are placeholders.

```sh
python3 Scripts/ffmpeg/media-tools.py proxy input.mov proxy.mp4
python3 Scripts/ffmpeg/media-tools.py split input.mov segments --seconds 30
python3 Scripts/ImageMagick/export-images.py studio originals exports --strip-metadata
python3 Scripts/ImageMagick/export-images.py jpeg originals small-jpegs --max-size 1000
```

FFmpeg split points are approximate because the script copies streams and cuts at keyframes. Image exports accept a new output directory and refuse conflicting input basenames. RAW, PSD and SVG support depends on local ImageMagick format support. A conversion error can leave partial outputs in the new destination.

## License

Scerno's original toolbox scripts use the [GNU General Public License v3](LICENSE).
The 123-reg DNS script retains its [upstream Unlicense](Scripts/DNS/123-reg-zonefile-creation.UNLICENSE).
