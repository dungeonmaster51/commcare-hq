from sqlagg.columns import *
from corehq.apps.reports.sqlreport import SqlTabularReport, DatabaseColumn
from corehq.apps.reports.fields import AsyncDrillableField, GroupField
from corehq.apps.reports.standard import CustomProjectReport, DatespanMixin
from corehq.apps.users.models import CommCareUser


class ProvinceField(AsyncDrillableField):
    label = "Province"
    slug = "province"
    hierarchy = [{"type": "province", "display": "name"}]


class CBOField(GroupField):
    name = 'CBO'
    default_option = 'All'


class CareReport(SqlTabularReport,
                 CustomProjectReport,
                 DatespanMixin):
    exportable = True
    emailable = True
    table_name = "care-ihapc-live_CareSAFluff"
    report_template_path = "care_sa/reports/grouped.html"

    show_age = True
    show_gender = True

    fields = [
        'corehq.apps.reports.fields.DatespanField',
        'care_sa.reports.sql.ProvinceField',
        'care_sa.reports.sql.CBOField',
    ]

    def selected_province(self):
        fixture = self.request.GET.get('fixture_id', "")
        return fixture.split(':')[1] if fixture else None

    def selected_cbo(self):
        group = self.request.GET.get('group', '')
        return group

    @property
    def filters(self):
        filters = [
            "domain = :domain",
            "date between :startdate and :enddate",
        ]

        if self.selected_province():
            filters.append("province = :province")
        if self.selected_cbo():
            filters.append("cbo = :cbo")

        return filters

    @property
    def group_by(self):
        groups = ['user_id']
        if self.show_age:
            groups.append('age_group')
        if self.show_gender:
            groups.append('gender')

        return groups

    @property
    def filter_values(self):
        return dict(
            domain=self.domain,
            startdate=self.datespan.startdate_param_utc,
            enddate=self.datespan.enddate_param_utc,
            province=self.selected_province(),
            cbo=self.selected_cbo(),
        )

    @property
    def columns(self):
        user = DatabaseColumn("User", "user_id", column_type=SimpleColumn)
        columns = [user]

        if not self.show_gender and not self.show_age:
            # hack: we have to give it a column type so there are no errors
            # but this isn't a column we let be auto populated anyway
            columns.append(DatabaseColumn("", "gender", column_type=SimpleColumn))
        if self.show_gender:
            columns.append(DatabaseColumn("Gender", "gender", column_type=SimpleColumn))
        if self.show_age:
            columns.append(DatabaseColumn("Age", "age_group", column_type=SimpleColumn))

        for column_attrs in self.report_columns:
            text, name = column_attrs[:2]
            name = '%s_total' % name
            if len(column_attrs) == 2:
                column = DatabaseColumn(text, name)
            else:
                # if there are more than 2 values, the third is the column
                # class override
                column = DatabaseColumn(text, name, column_attrs[2])

            columns.append(column)

        return columns

    @property
    def keys(self):
        [self.domain]

    @property
    def rows(self):
        rows = list(super(CareReport, self).rows)

        result = []
        for row in rows:
            u = CommCareUser.get_by_user_id(row.pop(0)['html'])
            group = {
                'username': u.username,
                'row_data': row,
            }

            if self.show_gender:
                gender = row.pop(0)
                group['gender'] = gender

            if self.show_age:
                age_group = row.pop(0)['html']
                if age_group == '0':
                    group['age_group'] = '0-14 years'
                elif age_group == '1':
                    group['age_group'] = '15-24 years'
                else:
                    group['age_group'] = '25+ years'

            if not self.show_gender and not self.show_age:
                # discard the gender column from blank header hack
                row.pop(0)
                group['gender'] = "no_grouping"

            result.append(group)

        return result

class TestingAndCounseling(CareReport):
    slug = 'tac'
    name = "Testing and Counseling"

    report_columns = [
        ['HIV Counseling', 'hiv_counseling'],
        ['Individuals HIV tested', 'hiv_tested'],
        ['Individuals HIV Positive ', 'hiv_positive'],
        ['Newly diagnosed HIV+ indv scr for TB', 'new_hiv_tb_screen'],  # 1d
        ['Individuals scr for TB [status unknown]', 'hiv_known_screened'],  # 1e
        #TODO NO DATA ['Individuals ref to PHCF with signs & symptoms of TB', 'referred_tb_signs'],  # 1f
        #['Individuals ref for TB diagnosis to PHCF who receive results', 'TODO'],  # 1g
        #TODO NO DATA ['Individuals HIV infected ref for CD4 count test in a PHCF', 'referred_for_cdf_new'],  # 1h
        ['Individuals HIV infected provided with CD4 count test results',
         'new_hiv_cd4_results'],  # 1i
        #TODO NO DATA ['Individuals HIV infected provided with CD4 count test results from previous months',
        # 'new_hiv_in_care_program'],  # 1k
        ['People tested as individuals', 'individual_tests'],  # 1l
        ['People tested as couples', 'couple_tests', SumColumn],  # 1m
    ]


class CareAndTBHIV(CareReport):
    slug = 'caretbhiv'
    name = "Care and TBHIV"

    report_columns = [
        ['Number of deceased patients', 'deceased'],  # 2a
        #['Number of patients lost to follow-up', TODO],  # 2b
        #not in form['Patients discharged from the program',  # 2c
        ['Patients completed TB treatment', 'tb_treatment_completed'],  # 2d
        #TODO NO DATA ['Existing HIV+ individuals who received CBC', 'received_cbc'],  # 2e
        #['New HIV+ individuals who received CBC', TODO],  # 2f
        # 2g
        ['HIV infected patients newly started on IPT', 'new_hiv_starting_ipt'],  # 2h
        ['HIV infected patients newly receiving Bactrim', 'new_hiv_starting_bactrim'],  # 2i
        #not in form['Clinically malnourished patients newly received therapeutic or supl food',  # 2j
        ['HIV+ patients receiving HIV care who are screened for symptoms of TB', 'hiv_on_care_screened_for_tb'],  # 2k
        ['Family members screened for symptoms of TB', 'family_screened'],  # 2l
    ]
