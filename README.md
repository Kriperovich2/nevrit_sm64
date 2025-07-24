# NERVIT
![Logo](Nevrit.png)

__**this program will literally just mve the png**__

# INSTALLATION
just go to [releases](https://github.com/Kriperovich2/nevrit_sm64/releases) bro

## Features

- **Texture Management**: Easily swap eye and cap logo textures
- **Bilingual Interface**: Supports English and Russian languages
- **Preview System**: Visual confirmation of textures before applying
- **Path Memory**: Remembers your last used folders between sessions

## System Requirements
- Windows 8+ 
- Python 3.10+ (maybe idk)
- Project 64 with any plugin like rice video or gliden64

## Usage

### First Launch
1. Run `Nevrit.exe`
2. Select your preferred language (English/Russian)
3. The program will create a `paths.json` file to remember your settings

### Interface Overview

#### Path Settings
- **hires_texture folder**: Set the path to your Super Mario 64 `hires_texture` folder
  - Example: `C:\projcet64\plugin\hires_texture\SUPER MARIO 64`
- **Textures folder**: Set the path to your custom textures folder containing:
  - `eyes` subfolder
  - `cap` subfolder

#### Preview Section
Displays thumbnails of available textures:
- Eye textures (3 variants)
- Cap logo texture

#### Control Buttons
1. **Move eyes**: Transfer eye textures to hires_texture folder
2. **Return eyes**: Restore eye textures to original location
3. **Move cap logo**: Transfer cap logo texture to hires_texture folder
4. **Return cap logo**: Restore cap logo texture to original location

## File Structure Requirements

### hires_texture Folder
Should contain the standard Super Mario 64 texture pack structure.

### Custom Textures Folder
Must contain these subfolders:
/textures_folder/
    ├── eyes/
    │   ├── SUPER MARIO 64#5D6B0678#0#2_all.png
    │   ├── SUPER MARIO 64#6B8D43C4#0#2_all.png
    │   └── SUPER MARIO 64#9FBECEF9#0#2_all.png
    └── cap/
        └── SUPER MARIO 64#905D3214#0#2_all.png

## Troubleshooting

**Problem**: Textures not showing in preview
- Solution: Verify your textures folder contains the correct subfolders and filenames

**Problem**: Buttons/text not in selected language
- Solution: Ensure both language JSON files are present in the program directory

## License

<a href="http://www.wtfpl.net/"><img
       src="http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png"
       width="80" height="15" alt="WTFPL" /></a>
