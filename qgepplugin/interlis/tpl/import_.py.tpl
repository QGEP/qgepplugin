from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from .. import utils

from .model_{{model_name}} import {{model_name|upper}}
from .model_{{ilimodel_name}} import {{ilimodel_name|upper}}


def import_():

    session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)

{% for class_to, classes_from in mapping.items() %}
    print("Importing {{classes_from|qualclassesnames}} -> {{model_name|upper}}.{{class_to.__name__}}")
{% if classes_from|length == 1 %}
    for row in session.query({{classes_from|qualclassesnames}}):
{% else %}
    for row, {{classes_from[1:]|classesnames}} in session.query({{classes_from|qualclassesnames}}){% if classes_from|length > 1 %}.join({{classes_from[1:]|qualclassesnames}}){% endif %}:
{% endif %}

{% for class_from in classes_from %}
        # AVAILABLE FIELDS IN {{class_from.__name__}}
{% for src_table, fields in class_from|classfields %}

        # --- {{src_table}} ---
        # {{fields|sort|join(", ")}}
{% endfor %}

{% endfor %}
        {{class_to.__name__}} = {{model_name|upper}}.{{class_to.__name__}}(
            # FIELDS TO MAP TO {{model_name|upper}}.{{class_to.__name__}}
{% for dst_table, fields in class_to|classfields %}
{% if dst_table != '_rel_' and dst_table != '_bwrel_' %}

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

{% endfor %}
    session.commit()

