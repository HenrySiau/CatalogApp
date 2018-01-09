"""
this module implement Json API
"""
from flask import Blueprint, jsonify, flash, redirect
from models import Catalog, Item


api_ = Blueprint('api_', __name__)


@api_.route('/catalog/<catalog_name>/items/json')
def catalog_items_json(catalog_name):
    """Return all items under this catalog with json format
    """
    catalog = Catalog.query.filter(Catalog.name == catalog_name).first()
    if catalog:
        return jsonify(Catalog=catalog.serialize)
    else:
        flash('there is no catalog named {}'.format(catalog_name))
        return redirect('/')


@api_.route('/item/<slug>/json')
def item_detail_json(slug):
    """Return information about this item with json format
        """
    item = Item.query.filter(Item.name == slug).first()
    if item:
        return jsonify(Item=item.serialize)
    else:
        flash('there is no Item named {}'.format(item.name))
        return redirect('/')
