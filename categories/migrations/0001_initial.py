# Generated by Django 4.1.3 on 2023-05-25 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='categories.category')),
                ('name', models.CharField(max_length=200, verbose_name='카테고리명')),
                ('depth', models.IntegerField(default=0)),
                ('user', models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='categories', to=settings.AUTH_USER_MODEL)),
                ('order', models.IntegerField(default=0, verbose_name='순서')),
                ('is_published', models.BooleanField(db_index=True, default=False, verbose_name='공개 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
            ],
            options={
                'db_table': 'categories',
                'ordering': ['parent__id', 'order'],
            },
        ),
    ]
