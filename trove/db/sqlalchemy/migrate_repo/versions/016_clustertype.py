#Copyright [2013] Rackspace

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.schema import MetaData

from trove.db.sqlalchemy.migrate_repo.schema import create_tables
from trove.db.sqlalchemy.migrate_repo.schema import DateTime
from trove.db.sqlalchemy.migrate_repo.schema import drop_tables
from trove.db.sqlalchemy.migrate_repo.schema import Integer
from trove.db.sqlalchemy.migrate_repo.schema import String
from trove.db.sqlalchemy.migrate_repo.schema import Table
from trove.db.sqlalchemy.migrate_repo.schema import Boolean

meta = MetaData()

clustertypes = Table(
    'clustertypes', meta,
    Column('id', String(36), primary_key=True, nullable=False),
    Column('name', String(255), nullable=False),
    Column('type', String(255), nullable=False),
    Column('max_instances', Integer()),
    Column('min_instances', Integer()),
    Column('deleted', Boolean(), default=0),
    Column('created', DateTime()),
    Column('updated', DateTime()),
    Column('deleted_at', DateTime()))

clustertype_data = {
    'id': '0c6941ba-e2f9-4d35-93b9-ac56588eaec7',
    'type': 'master-slave',
    'name': 'Master/Slave Replication/Clustering',
    'max_instances': 5,
    'min_instances': 3,
    'created': datetime.utcnow()
}


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    create_tables([clustertypes, ])
    clustertype_tbl = Table('clustertypes', meta, autoload=True)
    clustertype_tbl.insert().values(clustertype_data).execute()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    drop_tables([clustertypes, ])
