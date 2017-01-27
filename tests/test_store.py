from addok.batch import process_documents
from addok.ds import DS


def index_document(doc):
    process_documents([doc])


def deindex_document(id_):
    process_documents([{'id': id_, '_action': 'delete'}])


doc = {
    'id': 'xxxx',
    'type': 'street',
    'name': ['Vernou-la-Celle-sur-Seine', 'Vernou'],
    'city': 'Paris',
    'lat': '49.32545',
    'lon': '4.2565'
}


def test_index_document():
    index_document(doc)
    with DS.conn as conn:
        assert conn.execute('SELECT * from addok').fetchone()[0] == 'd|xxxx'


def test_fetch_document():
    index_document(doc)
    id_ = b'd|xxxx'
    assert list(DS.fetch(id_))[0][0] == id_


def test_add_document():
    data = ('d|xxxx', b'123')
    DS.add(data)
    with DS.conn as conn:
        assert conn.execute('SELECT * from addok').fetchone() == data


def test_remove_document():
    data = ('d|xxxx', b'123')
    DS.add(data)
    DS.remove(data[0])
    with DS.conn as conn:
        assert conn.execute('SELECT * from addok').fetchone() is None


def test_deindex_document():
    index_document(doc)
    deindex_document(doc['id'])
    with DS.conn as conn:
        assert conn.execute('SELECT * from addok').fetchone() is None
