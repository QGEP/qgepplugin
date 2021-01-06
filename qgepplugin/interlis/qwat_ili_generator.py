"""
This script is a STUB code generator, helping to implement QWAT/QGEP -> ILI migrations scripts.

The script will generate stub classes in  code in `qwat_ili_generator/output`.

ABANDONNED : doesn't make sense to generate classes directly from the ILI file if we use ILI2DB, as 
there are some specific ILI2DB fields that will be missing (t_ili fields).
"""

import sys
import re
import os

from . import config


def generate(interlis_path, interlis_path_translated=None):

    output_path = os.path.join(os.path.dirname(__file__), 'qwat_ili_generator_output', f'automap_base.py')
    output_handle = open(output_path, 'w', newline='\n')
    output_handle.write("from sqlalchemy.ext.automap import automap_base\n")
    output_handle.write("AutomapBase = automap_base()\n")
    output_handle.close()
    
    current_model = None

    def extract_imports(lines):
        nonlocal current_model

    def extract_class_def(lines):
        nonlocal current_model
        current_imports = []

        for line in lines:
            pattern_model = r'(TYPE )?MODEL ([a-zA-Z0-9_]+)'
            matches = re.match(pattern_model, line.strip())
            if matches:
                current_imports = []
                current_model = matches.group(2)

            pattern_import = r'IMPORTS ([a-zA-Z0-9_]+);'
            matches = re.match(pattern_import, line.strip())
            if matches:
                if matches.group(1) != "Units":
                    current_imports.append(matches.group(1))

            pattern = r'CLASS ([a-zA-Z0-9_]+)( \(ABSTRACT\))?( EXTENDS )?([a-zA-Z0-9_\.]+)?'
            matches = re.match(pattern, line.strip())
            if matches:
                classname = matches.group(1)
                is_abstract = True if matches.group(2) else False
                parent_classname = matches.group(4) or "AutomapBase"
                yield current_model, classname, is_abstract, parent_classname, current_imports

    if interlis_path_translated:
        translations = []
        translated_contents = open(interlis_path_translated, "r").read().splitlines()
        for current_model, classname, abstract, parent_classname, imports in extract_class_def(translated_contents):
            translations.append(classname)
            translations.append(parent_classname)

    i = 0
    output_handles = {}
    contents = open(interlis_path, "r").read().splitlines()
    for current_model, classname, is_abstract, parent_classname, imports in extract_class_def(contents):
        abstract = "# ABSTRACT !\n" if is_abstract else ""

        if current_model not in output_handles:
            output_path = os.path.join(os.path.dirname(__file__), 'qwat_ili_generator_output', f'{current_model}.py')
            output_handles[current_model] = open(output_path, 'w', newline='\n')
            output_handles[current_model].write(
                f"from .automap_base import AutomapBase\n"
            )
            for import_ in imports:
                output_handles[current_model].write(
                    f"from . import {import_}\n"
                )
            output_handles[current_model].write("\n\n")
        translation_comment = f"  # {translations[i]}({translations[i+1]})" if interlis_path_translated else ""
        output_handles[current_model].write(
            f"{abstract}"
            f"class {classname}({parent_classname}):{translation_comment}\n"
            f"    __tablename__ = '{classname.lower()}'\n"
            f"    __table_args__ = {{'schema': '{config.WASSER_SCHEMA}'}}\n"
            "\n"
        )
        i += 2
