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
    def create_metaattributes(row, session):
        metaattribute = {{ilimodel_name|upper}}.metaattribute(
            # FIELDS TO MAP TO {{ilimodel_name|upper}}.metaattribute
            # --- metaattribute ---
            # datenherr=row.REPLACE_ME,
            # datenlieferant=row.REPLACE_ME,
            # letzte_aenderung=row.REPLACE_ME,
            # sia405_baseclass_metaattribute=row.REPLACE_ME,
            # t_id=row.REPLACE_ME
            # t_seq=row.REPLACE_ME,
        )
        session.add(metaattribute)

{% for class_from, classes_to in mapping.items() %}
    print("Exporting {{model_name|upper}}.{{class_from.__name__}} -> {{classes_to|qualclassesnames}}")
    for row in session.query({{model_name|upper}}.{{class_from.__name__}}):
        # AVAILABLE FIELDS IN {{model_name|upper}}.{{class_from.__name__}}

{% for src_table, fields in class_from|classfields %}
        # --- {{src_table}} ---
        # {{fields|sort|join(", ")}}

{% endfor %}
{% for class_to in classes_to %}
{% if class_to.__name__ == 'metaattribute' %}
        create_metaattributes(row, session)
{% else %}
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
{% endif %}
{% endfor %}
        print(".", end="")
    print("done")
    session.flush()

{% endfor %}
    session.commit()


###############################################
# Import                                      #
###############################################

def import_():

    session = Session(utils.create_engine())
    tid_maker = utils.TidMaker(id_attribute='obj_id')

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
    session.flush()

{% endfor %}
    session.commit()

