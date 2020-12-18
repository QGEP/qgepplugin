"""
This script is a STUB code generator, helping to implement QWAT/QGEP -> ILI migrations scripts.

The script will generate stub classes in  code in `qwat_ili_generator/output`.
"""

import sys
import re
import os


def generate(interlis_path, interlis_path_translated=None):
    
    current_model = None

    def extract_class_def(lines):
        nonlocal current_model

        for line in lines:
            pattern_model = r'(TYPE )?MODEL ([a-zA-Z0-9_]+)'
            matches = re.match(pattern_model, line.strip())
            if matches:
                current_model = matches.group(2)

            pattern = r'CLASS ([a-zA-Z0-9_]+)( \(ABSTRACT\))?( EXTENDS )?([a-zA-Z0-9_\.]+)?'
            matches = re.match(pattern, line.strip())
            if matches:
                classname = matches.group(1)
                is_abstract = True if matches.group(2) else False
                parent_classname = matches.group(4)
                yield current_model, classname, is_abstract, parent_classname

    translations = []
    translated_contents = open(interlis_path_translated, "r").read().splitlines()
    for curruent_model, classname, abstract, parent_classname in extract_class_def(translated_contents):
        translations.append(classname)
        translations.append(parent_classname)

    i = 0
    output_handles = {}
    contents = open(interlis_path, "r").read().splitlines()
    for current_model, classname, is_abstract, parent_classname in extract_class_def(contents):
        classname_tr = translations[i]
        parent_classname_tr = translations[i+1]
        i += 2
        abstract = "# ABSTRACT !\n" if is_abstract else ""

        if current_model not in output_handles:
            output_path = os.path.join(os.path.dirname(__file__), 'qwat_ili_generator_output', f'{current_model}.py')
            output_handles[current_model] = open(output_path, 'w', newline='\n')
        output_handles[current_model].write(
            f"{abstract}"
            f"class {classname}({parent_classname}):  # {classname_tr}({parent_classname_tr})\n"
            "    pass\n"
            "\n"
        )
