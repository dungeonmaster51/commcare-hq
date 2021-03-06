# Generated by Django 2.2.13 on 2020-07-30 18:59

from django.db import migrations
from corehq.util.django_migrations import skip_on_fresh_install


@skip_on_fresh_install
def back_populate(apps, schema_editor):
    HqDeploy = apps.get_model('hqadmin', 'hqdeploy')
    for deploy in HqDeploy.objects.all():
        if deploy.diff_url and not deploy.commit:
            deploy.commit = _get_commit_from_url(deploy.diff_url)
            deploy.save()


def _get_commit_from_url(diff_url):
    try:
        ref_comparison = diff_url.split('/')[-1]
        last_deploy_sha, current_deploy_sha = ref_comparison.split('...')
        return current_deploy_sha
    except ValueError:
        # print('not a real diff_url', diff_url)
        return None


class Migration(migrations.Migration):

    dependencies = [
        ('hqadmin', '0017_hqdeploy_commit'),
    ]

    operations = [
        migrations.RunPython(
            back_populate, reverse_code=migrations.RunPython.noop, elidable=True),
    ]
