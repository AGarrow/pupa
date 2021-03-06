from pupa.core import db
from .base import BaseImporter


class EventImporter(BaseImporter):
    _type = 'event'

    def get_db_spec(self, event):
        spec = {
            "description": event['description'],
            "when": event['when'],
            'jurisdiction_id': event['jurisdiction_id'],
        }
        return spec


    def prepare_object_from_json(self, obj):

        def person(obj, what):
            spec = {}
            spec['session'] = obj['session']
            if 'chamber' in what:
                spec['chamber'] = what['chamber']
            spec['name'] = what['entity']
            # needs to get the right session (current)
            return spec

        def bill(obj, what):
            spec = {}
            spec['session'] = obj['session']
            if 'chamber' in what:
                spec['chamber'] = what['chamber']
            spec['bill_id'] = what['entity']
            # needs to get the right session (current)
            return spec

        def org(obj, what):
            spec = {}
            spec['session'] = obj['session']
            if 'chamber' in what:
                spec['chamber'] = what['chamber']
            spec['name'] = what['entity']
            # needs to get the right session (current)
            return spec

        spec_generators = {
            "person": person,
            "bill": bill,
            "organization": org,
        }

        # XXX participants

        for item in obj['agenda']:
            for entity in item['related_entities']:
                handler = spec_generators[entity['entity_type']]
                spec = handler(obj, entity)
                spec['jurisdiction_id'] = obj['jurisdiction_id']
                rel_obj = db.events.find_one(spec)
                if rel_obj:
                    entity['entity_id'] = rel_obj['_id']
                else:
                    self.logger.warning('Unknown related entity: {entity} '
                                        '({entity_type})'.format(**entity))
        return obj
