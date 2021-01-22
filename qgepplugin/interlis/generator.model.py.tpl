from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from . import utils
from . import config

from .datamodels.{{model}} import Classes as {{model|upper}}
from .datamodels.{{ilimodel}} import Classes as {{ilimodel|upper}}


###############################################
# Export
###############################################

def export():
{% for class_from, classes_to in TABLE_MAPPING.items() %}
    ###############################################
    # {{model|upper}}.{{class_from.__name__}} -> {{classes_to|classesnames}}
    ###############################################
    print("Exporting {{model|upper}}.{{class_from.__name__}} -> {{classes_to|classesnames}}")
    for row in session.query({{model|upper}}.{{class_from.__name__}}):    
        # AVAILABLE FIELDS IN {{model|upper}}.{{class_from.__name__}}

{% for src_table, fields in class_from|classfields %}
        # --- {{src_table}} ---
        # {{fields|join(", ")}}

{% endfor %}
{% for class_to in classes_to %}
        {{class_to.__name__}} = {{ilimodel|upper}}.{{class_to.__name__}}(
{% for dst_table, fields in class_to|classfields %}
            # --- {{dst_table}} ---
{% for field in fields %}
            # {{field}}=row.REPLACE_ME,
{% endfor %}

{% endfor %}
        )
{% endfor %}
{% endfor %}


###############################################
# Import
###############################################

def import_():
    pass