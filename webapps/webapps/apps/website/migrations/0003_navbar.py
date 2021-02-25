# Generated by Django 3.1.6 on 2021-02-25 12:30

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Navbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('navigation_links', wagtail.core.fields.StreamField([('NonDropdown', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock(max_length=255)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_url', wagtail.core.blocks.URLBlock(help_text='External URL will be prioritized over page link', required=False))])), ('Dropdown', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock(max_length=255)), ('sub_links', wagtail.core.blocks.StreamBlock([('SubLink', wagtail.core.blocks.StructBlock([('display_text', wagtail.core.blocks.CharBlock(max_length=255)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('external_url', wagtail.core.blocks.URLBlock(help_text='External URL will be prioritized over page link', required=False))]))]))]))], blank=True)),
            ],
            options={
                'verbose_name': 'Navigation Bar',
            },
        ),
    ]
