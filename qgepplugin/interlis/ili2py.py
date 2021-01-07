"""
This script is a BASIC interlis file parser.
"""

import re


class Ili2PyClass:

    def __init__(self, ili2py, model_name, class_name, parent_class_name, abstract, attributes):
        self.ili2py = ili2py
        self.model_name = model_name
        self.class_name = class_name
        if parent_class_name:
            if '.' in parent_class_name:
                self.parent_qual_name = parent_class_name
            else:
                self.parent_qual_name = f'{model_name}.{parent_class_name}'
        else:
            self.parent_qual_name = None
        self.abstract = abstract
        self.attributes = attributes

    @property
    def qual_name(self):
        return f"{self.model_name}.{self.class_name}"

    @property
    def parent(self):
        if not self.parent_qual_name:
            return None
        return self.ili2py.classes[self.parent_qual_name]

    @property
    def all_attributes(self):
        for attribute in self.attributes:
            yield self.qual_name, attribute
        if self.parent:
            yield from self.parent.all_attributes


class Ili2Py:

    def __init__(self, interlis_paths):

        self.classes = {}
        for interlis_path in interlis_paths:

            current_model = None
            current_class = None
            for line in open(interlis_path, "r").read().splitlines():

                # We enter in a new model
                pattern_model = r'(TYPE )?MODEL ([a-zA-Z0-9_]+)'
                matches = re.match(pattern_model, line.strip())
                if matches:
                    # current_imports = []
                    current_model = matches.group(2)
                    current_class = None

                # # A new import (ignored for now)
                # pattern_import = r'IMPORTS ([a-zA-Z0-9_]+);'
                # matches = re.match(pattern_import, line.strip())
                # if matches:
                #     if matches.group(1) != "Units":
                #         current_imports.append(matches.group(1))

                # We found a new class
                pattern = r'CLASS ([a-zA-Z0-9_]+)( \(ABSTRACT\))?( EXTENDS )?([a-zA-Z0-9_\.]+)?'
                matches = re.match(pattern, line.strip())
                if matches:
                    class_name = matches.group(1)
                    is_abstract = True if matches.group(2) else False
                    parent_class_name = matches.group(4)
                    current_class = Ili2PyClass(self, current_model, class_name, parent_class_name, is_abstract, [])
                    self.classes[current_class.qual_name] = current_class

                if current_class:
                    # We finished the class
                    pattern = f'END {current_class.class_name};'
                    matches = re.match(pattern, line.strip())
                    if matches:
                        current_class = None

                    # We found an attribute
                    pattern = r'([a-zA-Z0-9_]+):'
                    matches = re.match(pattern, line.strip())
                    if matches:
                        current_class.attributes.append(matches.group(1))

    def __str__(self):
        retval = ""
        for qual_name, class_ in self.classes.items():
            retval += f"{qual_name}\n"
            prev_src_class = qual_name
            for src_class, attribute in class_.all_attributes:
                if prev_src_class != src_class:
                    retval += f"  -- inherited from {src_class}\n"
                    prev_src_class = src_class
                retval += f"  {attribute}\n"
        return retval
