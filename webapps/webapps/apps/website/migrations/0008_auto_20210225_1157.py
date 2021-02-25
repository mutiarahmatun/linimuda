# Generated by Django 3.1.6 on 2021-02-25 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coderedcms', '0019_spelling_corrections'),
        ('wagtailcore', '0059_apply_collection_ordering'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('website', '0007_formconfirmemail_formpage_formpagefield_webpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formpage',
            name='coderedpage_ptr',
        ),
        migrations.RemoveField(
            model_name='formpage',
            name='thank_you_page',
        ),
        migrations.RemoveField(
            model_name='formpagefield',
            name='page',
        ),
        migrations.RemoveField(
            model_name='webpage',
            name='coderedpage_ptr',
        ),
        migrations.DeleteModel(
            name='FormConfirmEmail',
        ),
        migrations.DeleteModel(
            name='FormPage',
        ),
        migrations.DeleteModel(
            name='FormPageField',
        ),
        migrations.DeleteModel(
            name='WebPage',
        ),
    ]
