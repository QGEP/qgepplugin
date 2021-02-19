import sqlalchemy
import pickle
import os
from sqlalchemy.orm import interfaces

from sqlalchemy.ext.automap import (
    name_for_collection_relationship,
    name_for_scalar_relationship,
    generate_relationship,
)

from .. import config


def create_engine():
    return sqlalchemy.create_engine(
        f"postgresql://{config.PGUSER}:{config.PGPASS}@{config.PGHOST}:5432/{config.PGDATABASE}"
    )


def custom_name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation (uses the class name and it's fk column name), avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    return f"{referred_cls.__name__}__BWREL_{constraint.columns.keys()[0]}"


def custom_name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    # This customizes the name for backwards relation (uses the fk column name), avoiding clashes for inherited classes.
    # See https://stackoverflow.com/a/48288656/13690651
    return f"{constraint.columns.keys()[0]}__REL"


def custom_generate_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    """
    Skips creating backwards relations to avoid adding instances twice with session.merge
    """
    if direction is interfaces.ONETOMANY and local_cls.__table__.schema == 'qgep_vl':
        # We skip creating backwards relations from value_lists as they can lead to adding instances twice
        return None
    return generate_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw)


def prepare_automap_base(base, schema):
    """
    Prepares the automap base by reflecting all the fields with some specific configuration for relationship and population Base.classes with manually defined classes (which for some reason isn't done by default)
    """

    # DOESN'T WORK, BUT CACHING WOULD BE GOOD
    # pickle_file = f'{__file__}.pickled'
    # reflect = True
    # if os.path.exists(pickle_file):
    #     with open(pickle_file, 'rb') as f:
    #         reflect = False
    #         base.metadata = pickle.load(f)

    base.prepare(
        create_engine(),
        reflect=True,
        schema=schema,
        name_for_collection_relationship=custom_name_for_collection_relationship,
        name_for_scalar_relationship=custom_name_for_scalar_relationship,
        generate_relationship=custom_generate_relationship,
    )

    # For some reason, automap_base doesn't add manually defined classes to Base.classes,
    # so we do it manually here
    def add_subclasses(Parent):
        for subclass in Parent.__subclasses__():
            if subclass.__name__ not in base.classes:
                base.classes[subclass.__name__] = subclass
            add_subclasses(subclass)

    add_subclasses(base)

    # DOESN'T WORK, BUT CACHING WOULD BE GOOD
    # with open(pickle_file, 'wb') as f:
    #     pickle.dump(base.metadata, f)
