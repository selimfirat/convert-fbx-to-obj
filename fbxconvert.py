import os
import zipfile

import fbx
import sys
import shutil

def unzip(file_name, extract_to):
    zip_ref = zipfile.ZipFile(file_name)
    zip_ref.extractall(extract_to)  # extract file to dir
    zip_ref.close()  # close file
    # os.remove(file_name)  # delete zipped file

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def zip(file_name):
    zipf = zipfile.ZipFile('./converted/' + file_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir( file_name + '/', zipf)
    zipf.close()

def fbx_to_obj(file_dir, file_name):
    # Create an SDK manager
    manager = fbx.FbxManager.Create()

    # Create a scene
    scene = fbx.FbxScene.Create(manager, "")

    # Create an importer object
    importer = fbx.FbxImporter.Create(manager, "")

    # Path to the .fbx file
    milfalcon = file_dir + file_name + ".fbx"

    # Specify the path and name of the file to be imported
    importstat = importer.Initialize(milfalcon, -1)

    importstat = importer.Import(scene)

    # Create an exporter object
    exporter = fbx.FbxExporter.Create(manager, "")

    save_path = file_dir + file_name + ".dae"

    # Specify the path and name of the file to be imported
    exportstat = exporter.Initialize(save_path, -1)

    exportstat = exporter.Export(scene)
    os.remove(milfalcon)

def remove_tmp(file_name):
    shutil.rmtree('./' + file_name)
    shutil.rmtree('./__MACOSX/')

args = sys.argv
file_names = args[1:]

for file_name in file_names:
    unzip('to_convert/' + file_name + '.zip', './')
    fbx_to_obj('./' + file_name + '/', file_name)
    zip(file_name)
    remove_tmp(file_name)
