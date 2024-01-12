# AutoPacker Tool - How to Use

This README provides instructions on how to use the AutoPacker tool to create a Minecraft resource pack for multiple Minecraft versions

## Prerequisites

Before using the AutoPacker tool, ensure that you have the following:

- [Python version 3.7 or higher](https://python.org/downloads)
- That's all !

## Configuration

The AutoPacker tool uses a configuration file to customize the resource pack. Open the `autopacker.manifest.apmf` file and modify the following parameters:

- `pack-version`: The version number of the resource pack. (any format)
- `pack-title`: The title of the resource pack. (For Minecraft)
- `pack-description`: A brief description of the resource pack. (For Minecraft)
- `pack-image`: The path to the pack image file. (must be a png file)
- `pack-folder`: The path to the pack folder. (Only the "assets" and other folders, ***not the pack.mcmeta and the pack image***)
- `minecraft-versions`: The compatible Minecraft versions (without spaces):
 - Range : 1.20-1.20.4 (all versions between 1.20 to 1.20.4 (1.20, 1.20.1, 1.20.2, 1.20.3, 1.20.4))
 - Single : 1.17.1;1.20.2 (only 1.17.1 and 1.20.2)
 - Combined : 1.17.1;1.20-1.20.4 (Simple to understand i think)

Example :
```
pack-version=2.0.1
pack-title=§1Better 3D Blocks
pack-description=§1Play§1 §6Minecraft§6... §2but§2 §fwith§f         §5more§5 §93§9§aD§a §4!!§4
pack-image=../pack.png
pack-folder=../v2.0.1
minecraft-versions=1.10-1.20.4
```

## Usage

To use the AutoPacker tool, follow these steps:

0. Edit the `autopacker.manifest.apmf` with your settings
1. Open a command prompt or terminal.
2. Navigate to the directory where the AutoPacker tool is located (`cd` and then the path).
3. Run the following command: `py main.py`.
4. The tool will automatically generate the resource packs based on the configuration file.
5. Once the process is complete, the resource packs will be available in the "Packs OK" folder.

Tool originally made for my [3D texture pack "Better 3D Blocks"](https://www.curseforge.com/minecraft/texture-packs/minecraft-3d-ressource-pack)
