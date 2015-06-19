from couchdbkit.ext.django.schema import StringProperty, ListProperty
from casexml.apps.case.models import CommCareCase
from dimagi.ext.couchdbkit import Document
from dimagi.utils.couch.database import iter_docs


class CommCareCaseGroup(Document):
    """
        This is a group of CommCareCases. Useful for managing cases in larger projects.
    """
    name = StringProperty()
    domain = StringProperty()
    cases = ListProperty()
    timezone = StringProperty()

    def get_time_zone(self):
        # Necessary for the CommCareCaseGroup to interact with CommConnect, as if using the CommCareMobileContactMixin
        # However, the entire mixin is not necessary.
        return self.timezone

    def get_cases(self, limit=None, skip=None):
        case_ids = self.cases
        if skip is not None:
            case_ids = case_ids[skip:]
        if limit is not None:
            case_ids = case_ids[:limit]
        for case_doc in iter_docs(CommCareCase.get_db(), case_ids):
            # don't let CommCareCase-Deleted get through
            if case_doc['doc_type'] == 'CommCareCase':
                yield CommCareCase.wrap(case_doc)

    def get_total_cases(self, clean_list=False):
        if clean_list:
            self.clean_cases()
        return len(self.cases)

    def clean_cases(self):
        cleaned_list = []
        for case_doc in iter_docs(CommCareCase.get_db(), self.cases):
            # don't let CommCareCase-Deleted get through
            if case_doc['doc_type'] == 'CommCareCase':
                cleaned_list.append(case_doc['_id'])
        if len(self.cases) != len(cleaned_list):
            self.cases = cleaned_list
            self.save()

    @classmethod
    def get_by_domain(cls, domain, limit=None, skip=None, include_docs=True):
        extra_kwargs = {}
        if limit is not None:
            extra_kwargs['limit'] = limit
        if skip is not None:
            extra_kwargs['skip'] = skip
        return cls.view(
            'case/groups_by_domain',
            startkey=[domain],
            endkey=[domain, {}],
            include_docs=include_docs,
            reduce=False,
            **extra_kwargs
        ).all()

    @classmethod
    def get_total(cls, domain):
        data = cls.get_db().view(
            'case/groups_by_domain',
            startkey=[domain],
            endkey=[domain, {}],
            reduce=True
        ).first()
        return data['value'] if data else 0
