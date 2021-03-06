""" these are helper classes for object creation during the scrape """
from larvae.person import Person
from larvae.organization import Organization
from larvae.membership import Membership


class Legislator(Person):
    _is_legislator = True
    __slots__ = ('district', 'party', 'chamber', '_contact_details')

    def __init__(self, name, district, party=None, chamber=None, **kwargs):
        super(Legislator, self).__init__(name, **kwargs)
        self.district = district
        self.party = party
        self.chamber = chamber
        self._contact_details = []

    def add_contact(self, type, value, note):
        self._contact_details.append({'type': type, 'value': value,
                                      'note': note})

    def add_committee_membership(self, com_name, role='member'):
        org = Organization(com_name, classification='committee')
        self.add_membership(org, role=role)
        self._related.append(org)


class Committee(Organization):

    def __init__(self, *args, **kwargs):
        super(Committee, self).__init__(*args, **kwargs)

    def add_member(self, name, role='member', **kwargs):
        member = Person(name)
        membership = Membership(member._id, self._id, role=role,
                                **kwargs)
        self._related.append(member)
        self._related.append(membership)
