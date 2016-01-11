import os
import sys
import transaction
import json

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Bargain,
    Supplier,
    Base,
)


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    connect_string = settings['sqlalchemy.url']\
        .replace('DBUser', os.environ['DBUSER'])\
        .replace('DBPassword', os.environ['DBPASSWORD'])
    settings['sqlalchemy.url'] = connect_string
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        store_data = json.loads(open('emporium/scripts/store_data.json').
                                read())

        suppliers = {}
        for item in store_data['suppliers']:
            supplier = Supplier(name=item['name'], tax_id=item['tax_id'])
            suppliers[supplier.name] = supplier
            DBSession.add(supplier)

        for item in store_data['bargains']:
            bargain = Bargain(
                sku=item['sku'],
                price=item['price'],
                supplier=suppliers[item['supplier_name']]
            )
            bargain.info = item['info']
            DBSession.add(bargain)
