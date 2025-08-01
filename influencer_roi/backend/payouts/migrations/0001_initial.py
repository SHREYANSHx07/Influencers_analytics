# Generated by Django 4.2.7 on 2025-07-26 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('influencers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basis', models.CharField(choices=[('post', 'Per Post'), ('order', 'Per Order'), ('revenue', 'Revenue Share'), ('flat', 'Flat Rate')], help_text='Basis for payout calculation', max_length=20)),
                ('rate', models.DecimalField(decimal_places=2, help_text='Rate per post/order/revenue share percentage', max_digits=10)),
                ('orders', models.IntegerField(default=0, help_text='Number of orders for this payout')),
                ('total_payout', models.DecimalField(decimal_places=2, help_text='Total payout amount', max_digits=10)),
                ('payout_date', models.DateField(help_text='Date of payout')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('influencer', models.ForeignKey(help_text='Associated influencer', on_delete=django.db.models.deletion.CASCADE, related_name='payouts', to='influencers.influencer')),
            ],
            options={
                'verbose_name': 'Payout',
                'verbose_name_plural': 'Payouts',
                'db_table': 'payouts',
                'ordering': ['-payout_date', '-created_at'],
            },
        ),
    ]
