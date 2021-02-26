# Generated by Django 3.0.10 on 2020-10-15 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coderedcms', '0018_auto_20200805_1702'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailimages', '0022_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleIndexPage',
            fields=[
                ('coderedpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coderedcms.CoderedPage')),
                ('show_images', models.BooleanField(default=True, verbose_name='Show images')),
                ('show_captions', models.BooleanField(default=True)),
                ('show_meta', models.BooleanField(default=True, verbose_name='Show author and date info')),
                ('show_preview_text', models.BooleanField(default=True, verbose_name='Show preview text')),
                ('hits', models.IntegerField(default=0, editable=False)),
                ('is_company_articles', models.BooleanField(default=False, help_text='Company articles adalah artikel-artikel mengenai Insanq. Misal: Konseling, Test Psikologi, Seminar & Training', verbose_name='Is this company articles?')),
            ],
            options={
                'verbose_name': 'Article Landing Page',
            },
            bases=('coderedcms.coderedpage',),
        ),
        migrations.CreateModel(
            name='ArticlePage',
            fields=[
                ('coderedpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='coderedcms.CoderedPage')),
                ('caption', models.CharField(blank=True, max_length=255, verbose_name='Caption')),
                ('author_display', models.CharField(blank=True, help_text='Override how the author’s name displays on this article.', max_length=255, verbose_name='Display author as')),
                ('date_display', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Publish date')),
                ('hits', models.IntegerField(default=0, editable=False)),
                ('body_text', wagtail.core.fields.RichTextField(verbose_name='body')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('main_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'verbose_name': 'Article Page',
                'ordering': ['-first_published_at'],
            },
            bases=('coderedcms.coderedpage',),
        ),
    ]
