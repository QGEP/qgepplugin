from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from . import utils

from .datamodels.{{model_name}} import Classes as {{model_name|upper}}
from .datamodels.{{ilimodel_name}} import Classes as {{ilimodel_name|upper}}


###############################################
# Export                                      #
###############################################

def export():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

{% for class_from, classes_to in mapping.items() %}
    print("Exporting {{model_name|upper}}.{{class_from.__name__}} -> {{classes_to|classesnames}}")
    for row in session.query({{model_name|upper}}.{{class_from.__name__}}):
        # AVAILABLE FIELDS IN {{model_name|upper}}.{{class_from.__name__}}

{% for src_table, fields in class_from|classfields %}
        # --- {{src_table}} ---
        # {{fields|sort|join(", ")}}

{% endfor %}
{% for class_to in classes_to %}
        {{class_to.__name__}} = {{ilimodel_name|upper}}.{{class_to.__name__}}(
            # FIELDS TO MAP TO {{ilimodel_name|upper}}.{{class_to.__name__}}
{% for dst_table, fields in class_to|classfields %}
{% if dst_table != '_relations_' %}
            # --- {{dst_table}} ---
{% for field in fields|sort %}
            # {{field}}=row.REPLACE_ME,
{% endfor %}

{% endif %}
{% endfor %}
        )
        session.add({{class_to.__name__}})
{% endfor %}
        print(".", end="")
    print("done")
    session.commit()

{% endfor %}


###############################################
# Import                                      #
###############################################

def import_():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

{% for class_to, classes_from in mapping.items() %}
    print("Importing {{classes_from|classesnames}} -> {{model_name|upper}}.{{class_to.__name__}}")
    for row in session.query({{ilimodel_name|upper}}.{{classes_from[0].__name__}}):
{% if classes_from|length > 1 %}
    # TODO : somehow join {{classes_from[1:]|classesnames}}
{% endif %}
        # AVAILABLE FIELDS IN {{ilimodel_name|upper}}.{{classes_from[0].__name__}}

{% for src_table, fields in classes_from[0]|classfields %}
        # --- {{src_table}} ---
        # {{fields|sort|join(", ")}}

{% endfor %}
        {{class_to.__name__}} = {{model_name|upper}}.{{class_to.__name__}}(
            # FIELDS TO MAP TO {{model_name|upper}}.{{class_to.__name__}}
{% for dst_table, fields in class_to|classfields %}
{% if dst_table != '_relations_' %}
            # --- {{dst_table}} ---
{% for field in fields|sort %}
            # {{field}}=row.REPLACE_ME,
{% endfor %}

{% endif %}
{% endfor %}
        )
        session.add({{class_to.__name__}})
        print(".", end="")
    print("done")
    session.commit()

{% endfor %}

