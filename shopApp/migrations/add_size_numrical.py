from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0007_homeslider_promotionalbanner_sitesettings_staticpage_and_more'),  # Use the last successful migration
    ]

    operations = [
        migrations.AddField(
            model_name='size',
            name='size_numrical',
            field=models.CharField(default='', max_length=10, verbose_name='سایز عددی نوشتاری'),
            preserve_default=False,
        ),
    ] 