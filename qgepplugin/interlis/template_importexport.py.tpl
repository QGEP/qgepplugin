from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

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
# Import
###############################################

def import_():
    pass
