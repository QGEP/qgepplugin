from sqlalchemy.orm import Session
from geoalchemy2.functions import ST_Transform, ST_Force2D

from .. import utils

from .model_{{model_name}} import {{model_name|upper}}
from .model_{{ilimodel_name}} import {{ilimodel_name|upper}}


def export():

    session = Session(utils.sqlalchemy.create_engine(), autocommit=False, autoflush=False)
    tid_maker = utils.ili2db.TidMaker(id_attribute='obj_id')

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
{% if dst_table != '_rel_' and dst_table != '_bwrel_' %}

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

{% endfor %}
    session.commit()
