import os
import shutil
import json
import zipfile

def load_manifest(file_path):
    manifest = {}
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split('=')
            manifest[key] = value
    return manifest

def load_pack_formats(file_path) -> dict[str, int]:
    pack_formats = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line in ('\n', '\r\n', '', '\t', '\n\t'):
                continue
            version, pack_format = line.strip().split(':')
            
            pack_formats[version] = int(pack_format)
    return pack_formats

def generate_pack_mcmeta(description, pack_format):
    # print(pack_format)
    return {
        "pack": {
            "pack_format": pack_format,
            "description": description
        }
    }

def get_target_folder(pack_title, pack_version, minecraft_versions):
    end_sentence = f"{minecraft_versions[0]}-{minecraft_versions[-1]}" if len(minecraft_versions) > 1 else minecraft_versions[0]
    
    target_folder = f"Packs OK/{pack_title.replace(' ', '.')}-v{pack_version}-{end_sentence}"
    return target_folder
    

def create_pack_folders(pack_title, pack_version, minecraft_versions, pack_folder, pack_image, pack_mcmeta):
    print("      Generating pack for Minecraft versions: ", end='')
    print(', '.join(minecraft_versions))
    
    target_folder = get_target_folder(pack_title, pack_version, minecraft_versions)
    os.makedirs(target_folder, exist_ok=True)
    
    with open(os.path.join(target_folder, 'pack.mcmeta'), 'w', encoding="utf-8") as file:
        # print(pack_mcmeta)
        json.dump(pack_mcmeta, file, indent=4)
    
    # Copy files from pack_folder to target_folder
    shutil.copytree(pack_folder, target_folder, dirs_exist_ok=True)

    # Copy pack image to the root of the pack folder
    shutil.copy(pack_image, target_folder)
    return target_folder


def get_mc_versions(mc_versions: str):
    global pack_formats
    
    minecraft_versions = []
    for version in mc_versions:
        print("  -", version)
        if "-" in version:
            # Get all versions between the specified range (like 1.16-1.17), based on the pack_formats file
            start, end = version.split('-')
            _formats = []
            start_add = False
            for format in list(reversed(list(pack_formats.keys()))):
                # print(format)
                if format == start:
                    start_add = True
                if start_add:
                    _formats.append(format)
                if format == end:
                    break
            # print(_formats)
            minecraft_versions.extend(_formats)
        else:
            minecraft_versions.append(version)
    
    return minecraft_versions

def cls():
    try:
        os.system("cls")
    except:
        try:
            os.system("clear")
        except:
            pass


if __name__ == "__main__":
    cls()
    
    print("Loading...")
    print("   Loading data...")
    global pack_formats
    global packs_paths
    
    manifest_path = "autopacker.manifest.apmf"
    formats_path = "packsformats.txt"

    print("   Loading manifest...")
    manifest = load_manifest(manifest_path)
    pack_formats = load_pack_formats(formats_path)
    packs_paths = []

    pack_title = manifest["pack-title"]
    pack_version = manifest["pack-version"]
    pack_description = manifest["pack-description"]
    pack_image = manifest["pack-image"]
    pack_folder = manifest["pack-folder"]
    mc_versions = manifest["minecraft-versions"].split(';')
    
    # print("   Loading pack files...")
    # for folder in os.listdir(pack_folder):
    #     packs_paths.append((folder, tuple(get_mc_versions(folder))))
    print("Loaded.")
    

    # Get the common pack_format for the specified Minecraft versions
    # print("Getting packs...")
    minecraft_versions = get_mc_versions(mc_versions)
    
    print(f"Generating packs for Minecraft versions: {', '.join(minecraft_versions)}.")
    
    common_pack_format = [pack_formats[v] for v in minecraft_versions]
    # print(f"Pack formats: {', '.join(str(v) for v in common_pack_format)}")
    
    already_listed_packs = []
    generated_packs = []
    print("Creating packs...")
    for i, version in enumerate(minecraft_versions):
        print(f"   Pack for {version}", end=" ")
        if common_pack_format[i] in already_listed_packs:
            print("already created, skipping...")
            continue
        print("is building :")
        generated_packs.append(common_pack_format[i])
        # print("\n" if i == len(minecraft_versions) - 1 else "")
        # print(common_pack_format[i])
        already_listed_packs.append(common_pack_format[i])
        pack_mcmeta = generate_pack_mcmeta(pack_description, common_pack_format[i])
        # print(pack_mcmeta)
        
        versions = [v for v in minecraft_versions if pack_formats[v] == common_pack_format[i]]
        target_folder = create_pack_folders(pack_title, pack_version, versions, pack_folder, pack_image, pack_mcmeta)
        print("      Pack generated.")
        print("      Zipping pack")
        
        
        global zipf, zipped_cnt
        zipf = zipfile.ZipFile(f"./{target_folder}.zip", "x")
        zipped_cnt = 0

        def zip_the_files(base, path):
            global zipf, zipped_cnt
            # print("\n", path)
            for f in os.listdir(f"./{path}"):
                # print(f)
                ac_path = f"{path}/{f}"
                if os.path.isfile(ac_path):
                    zipf.write(ac_path, arcname=ac_path.replace(base, ""))
                    # print(f"is a file  {ac_path}")
                    zipped_cnt += 1
                    continue
                
                # print(f"is a dir  {ac_path}")
                zipf.write(ac_path, arcname=ac_path.replace(base, ""))
                zipped_cnt += 1
                zip_the_files(base, path=ac_path)
        
        zip_the_files(base=target_folder, path=target_folder)
        
        zipf.close()
        print(f"      Pack zipped. {zipped_cnt} file{'s' if zipped_cnt > 1 else ''} zipped")
        del zipf, zipped_cnt
        
        
    
    print("✅ Packs generated successfully.")
