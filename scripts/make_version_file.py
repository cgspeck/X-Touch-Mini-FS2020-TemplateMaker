import pyinstaller_versionfile

from template_maker import version

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version=str(version.VERSION),
    file_description="Makes templates for X-Touch Mini",
    internal_name="Xtouch Template Maker",
    legal_copyright="Copyright (C) 2023 Chris Speck",
    original_filename="Xtouch Template Maker.exe",
    product_name="X-Touch Mini FS2020 Template Maker",
    translations=[0, 1200],
)
