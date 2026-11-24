# Windows drag-and-drop scripts

Download the toolbox and extract it locally. In Windows Explorer, drag the items described below onto the corresponding `.bat` file. Each script leaves its window open so you can read the result.

| Batch file | What to drop | What it does |
| --- | --- | --- |
| [Export studio images](ImageMagick/Export%20studio%20images.bat) | JPG, JPEG, PNG, TIFF, PSD, or WebP files, folders containing those images, or a mix | Creates eight print and web image variants. Requires ImageMagick 7 with `magick.exe` on your PATH. |
| [Copy selected images](File%20Management/Copy%20selected%20images.bat) | Image files you have selected in Explorer | Copies them to `Selected Images` beside the originals. Existing names are skipped. |
| [Create Product Project Folders](Folder%20Templates/Create%20Product%20Project%20Folders.bat) | One existing parent folder | Creates a product folder for specifications, manuals, certification, graphics and media. |
| [Create Location Shoot Folders](Folder%20Templates/Create%20Location%20Shoot%20Folders.bat) | One existing parent folder | Creates originals, selects, editing and export folders for a location shoot. |
| [Create Studio Shoot Folders](Folder%20Templates/Create%20Studio%20Shoot%20Folders.bat) | One existing parent folder | Creates a studio workflow with corrected images, editing and print and web exports. |
| [Create Image Selection Folders](Folder%20Templates/Create%20Image%20Selection%20Folders.bat) | One existing parent folder | Creates a short originals, selects, working and exports layout for any image set. |

The studio exporter processes the immediate files in each dropped folder and writes a `Studio Exports` subfolder. A file dropped by itself gets a sibling export folder named after the full input filename. Export filenames keep the source extension before the output extension, so `image.psd` and `image.png` can both produce JPEGs without colliding. The exporter leaves existing export folders alone. A failed conversion can leave partial outputs in a newly created folder.

The copy utility uses the files you select. The old 5D file was empty, so this version does not assume a particular app or read star ratings. The folder templates can run again against the same parent and preserve existing content.
