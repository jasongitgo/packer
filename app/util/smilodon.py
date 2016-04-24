import datetime
import math
import uuid

from flask import request
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.ext import hybrid
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.inspection import inspect as sqlalchemy_inspect
from sqlalchemy.orm import RelationshipProperty as RelProperty
from sqlalchemy.orm.query import Query

#: Names of columns which should definitely not be considered user columns to
#: be included in a dictionary representation of a model.
COLUMN_BLACKLIST = ('_sa_polymorphic_on',)
#: Names of attributes which should definitely not be considered relations when
#: dynamically computing a list of relations of a SQLAlchemy model.
RELATION_BLACKLIST = ('query', 'query_class', '_sa_class_manager',
                      '_decl_class_registry')


def model_to_dict(inst):
    model = inst.__class__
    relations = frozenset(get_relations(model))
    # do not follow relations that will not be included in the response
    include_columns = None
    exclude_columns = None
    include_relations = None
    include_methods = None
    exclude_relations = None
    if include_columns is not None:
        cols = frozenset(include_columns)
        rels = frozenset(include_relations)
        relations &= (cols | rels)
    elif exclude_columns is not None:
        relations -= frozenset(exclude_columns)
    deep = dict((r, {}) for r in relations)
    return to_dict(inst, deep)


# This code was adapted from :meth:`elixir.entity.Entity.to_dict` and
# http://stackoverflow.com/q/1958219/108197.
def to_dict(instance, deep=None, exclude=None, include=None,
            exclude_relations=None, include_relations=None,
            include_methods=None):
    """Returns a dictionary representing the fields of the specified `instance`
    of a SQLAlchemy model.

    The returned dictionary is suitable as an argument to
    :func:`flask.jsonify`; :class:`datetime.date` and :class:`uuid.UUID`
    objects are converted to string representations, so no special JSON encoder
    behavior is required.

    `deep` is a dictionary containing a mapping from a relation name (for a
    relation of `instance`) to either a list or a dictionary. This is a
    recursive structure which represents the `deep` argument when calling
    :func:`!_to_dict` on related instances. When an empty list is encountered,
    :func:`!_to_dict` returns a list of the string representations of the
    related instances.

    If either `include` or `exclude` is not ``None``, exactly one of them must
    be specified. If both are not ``None``, then this function will raise a
    :exc:`ValueError`. `exclude` must be a list of strings specifying the
    columns which will *not* be present in the returned dictionary
    representation of the object (in other words, it is a
    blacklist). Similarly, `include` specifies the only columns which will be
    present in the returned dictionary (in other words, it is a whitelist).

    .. note::

       If `include` is an iterable of length zero (like the empty tuple or the
       empty list), then the returned dictionary will be empty. If `include` is
       ``None``, then the returned dictionary will include all columns not
       excluded by `exclude`.

    `include_relations` is a dictionary mapping strings representing relation
    fields on the specified `instance` to a list of strings representing the
    names of fields on the related model which should be included in the
    returned dictionary; `exclude_relations` is similar.

    `include_methods` is a list mapping strings to method names which will
    be called and their return values added to the returned dictionary.

    """
    if (exclude is not None or exclude_relations is not None) and \
            (include is not None or include_relations is not None):
        raise ValueError('Cannot specify both include and exclude.')
    # create a list of names of columns, including hybrid properties
    instance_type = type(instance)
    columns = []
    try:
        inspected_instance = sqlalchemy_inspect(instance_type)
        column_attrs = inspected_instance.column_attrs.keys()
        descriptors = inspected_instance.all_orm_descriptors.items()
        hybrid_columns = [k for k, d in descriptors
                          if d.extension_type == hybrid.HYBRID_PROPERTY
                          and not (deep and k in deep)]
        columns = column_attrs + hybrid_columns
    except NoInspectionAvailable:
        return instance
    # filter the columns based on exclude and include values
    if exclude is not None:
        columns = (c for c in columns if c not in exclude)
    elif include is not None:
        columns = (c for c in columns if c in include)
    # create a dictionary mapping column name to value
    result = dict((col, getattr(instance, col)) for col in columns
                  if not (col.startswith('__') or col in COLUMN_BLACKLIST))
    # add any included methods
    if include_methods is not None:
        for method in include_methods:
            if '.' not in method:
                value = getattr(instance, method)
                # Allow properties and static attributes in include_methods
                if callable(value):
                    value = value()
                result[method] = value
    # Check for objects in the dictionary that may not be serializable by
    # default. Convert datetime objects to ISO 8601 format, convert UUID
    # objects to hexadecimal strings, etc.
    for key, value in result.items():
        if isinstance(value, (datetime.date, datetime.time)):
            result[key] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            result[key] = str(value)
        elif key not in column_attrs and is_mapped_class(type(value)):
            result[key] = to_dict(value)
    # recursively call _to_dict on each of the `deep` relations
    deep = deep or {}
    for relation, rdeep in deep.items():
        # Get the related value so we can see if it is None, a list, a query
        # (as specified by a dynamic relationship loader), or an actual
        # instance of a model.
        relatedvalue = getattr(instance, relation)
        if relatedvalue is None:
            result[relation] = None
            continue
        # Determine the included and excluded fields for the related model.
        newexclude = None
        newinclude = None
        if exclude_relations is not None and relation in exclude_relations:
            newexclude = exclude_relations[relation]
        elif (include_relations is not None and
                      relation in include_relations):
            newinclude = include_relations[relation]
        # Determine the included methods for the related model.
        newmethods = None
        if include_methods is not None:
            newmethods = [method.split('.', 1)[1] for method in include_methods
                          if method.split('.', 1)[0] == relation]
        if is_like_list(instance, relation):
            result[relation] = [to_dict(inst, rdeep, exclude=newexclude,
                                        include=newinclude,
                                        include_methods=newmethods)
                                for inst in relatedvalue]
            continue
        # If the related value is dynamically loaded, resolve the query to get
        # the single instance.
        if isinstance(relatedvalue, Query):
            relatedvalue = relatedvalue.one()
        result[relation] = to_dict(relatedvalue, rdeep, exclude=newexclude,
                                   include=newinclude,
                                   include_methods=newmethods)
    return result


def is_mapped_class(cls):
    """Returns ``True`` if and only if the specified SQLAlchemy model class is
    a mapped class.

    """
    try:
        sqlalchemy_inspect(cls)
        return True
    except:
        return False


def is_like_list(instance, relation):
    """Returns ``True`` if and only if the relation of `instance` whose name is
    `relation` is list-like.

    A relation may be like a list if, for example, it is a non-lazy one-to-many
    relation, or it is a dynamically loaded one-to-many.

    """
    if relation in instance._sa_class_manager:
        return instance._sa_class_manager[relation].property.uselist
    elif hasattr(instance, relation):
        attr = getattr(instance._sa_instance_state.class_, relation)
        if hasattr(attr, 'property'):
            return attr.property.uselist
    related_value = getattr(type(instance), relation, None)
    if isinstance(related_value, AssociationProxy):
        local_prop = related_value.local_attr.prop
        if isinstance(local_prop, RelProperty):
            return local_prop.uselist
    return False


def get_relations(model):
    """Returns a list of relation names of `model` (as a list of strings)."""
    return [k for k in dir(model)
            if not (k.startswith('__') or k in RELATION_BLACKLIST)
            and get_related_model(model, k)]


def get_related_model(model, relationname):
    """Gets the class of the model to which `model` is related by the attribute
    whose name is `relationname`.

    """
    if hasattr(model, relationname):
        attr = getattr(model, relationname)
        if hasattr(attr, 'property') \
                and isinstance(attr.property, RelProperty):
            return attr.property.mapper.class_
        if isinstance(attr, AssociationProxy):
            return get_related_association_proxy_model(attr)
    return None


def get_related_association_proxy_model(attr):
    """Returns the model class specified by the given SQLAlchemy relation
    attribute, or ``None`` if no such class can be inferred.

    `attr` must be a relation attribute corresponding to an association proxy.

    """
    prop = attr.remote_attr.property
    for attribute in ('mapper', 'parent'):
        if hasattr(prop, attribute):
            return getattr(prop, attribute).class_
    return None


def list_to_dict(instances):
    if isinstance(instances, list):
        num_results = len(instances)
    results_per_page = 10
    if results_per_page > 0:
        # get the page number (first page is page 1)
        page_num = int(request.args.get('page', 1))
        start = (page_num - 1) * results_per_page
        end = min(num_results, start + results_per_page)
        total_pages = int(math.ceil(num_results / results_per_page))
    else:
        page_num = 1
        start = 0
        end = num_results
        total_pages = 1
    objects = [model_to_dict(x)
               for x in instances[start:end]]
    return dict(page=page_num, objects=objects, total_pages=total_pages,
                num_results=num_results)
