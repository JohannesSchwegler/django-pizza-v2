# Generated by Django 3.0.3 on 2020-02-21 20:58

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='DinnerPlatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='DinnerPlatterName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(default='no_photo_available.png', upload_to='')),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(default='no_photo_available.png', upload_to='')),
                ('description', models.TextField(default='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Salad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(default='no_photo_available.png', upload_to='')),
                ('description', models.TextField(default='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='SubAddon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='SubName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('image', models.ImageField(default='no_photo_available.png', upload_to='')),
                ('description', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='pizza',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.AddField(
            model_name='order',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='order_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pizzaname',
            name='image',
            field=models.ImageField(default='no_photo_available.png', upload_to=''),
        ),
        migrations.CreateModel(
            name='Sub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='no_photo_available.png', upload_to='')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=4)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='orders.SubName')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='orders.Size')),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toppings_count', models.PositiveSmallIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=4)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizzas', to='orders.PizzaName')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizzas', to='orders.Size')),
            ],
        ),
        migrations.CreateModel(
            name='OrderSub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Sub')),
                ('sub_addons', models.ManyToManyField(blank=True, to='orders.SubAddon')),
            ],
        ),
        migrations.CreateModel(
            name='OrderSalad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('salad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Salad')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Pizza')),
                ('toppings', models.ManyToManyField(to='orders.Topping')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('pasta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Pasta')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDinnerPlatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('dinner_platter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.DinnerPlatter')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
            ],
        ),
        migrations.AddField(
            model_name='dinnerplatter',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinner_platters', to='orders.DinnerPlatterName'),
        ),
        migrations.AddField(
            model_name='dinnerplatter',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinner_platters', to='orders.Size'),
        ),
        migrations.AddField(
            model_name='order',
            name='dinner_platters',
            field=models.ManyToManyField(blank=True, through='orders.OrderDinnerPlatter', to='orders.DinnerPlatter'),
        ),
        migrations.AddField(
            model_name='order',
            name='pastas',
            field=models.ManyToManyField(blank=True, through='orders.OrderPasta', to='orders.Pasta'),
        ),
        migrations.AddField(
            model_name='order',
            name='pizzas',
            field=models.ManyToManyField(through='orders.OrderPizza', to='orders.Pizza'),
        ),
        migrations.AddField(
            model_name='order',
            name='salads',
            field=models.ManyToManyField(blank=True, through='orders.OrderSalad', to='orders.Salad'),
        ),
        migrations.AddField(
            model_name='order',
            name='subs',
            field=models.ManyToManyField(blank=True, through='orders.OrderSub', to='orders.Sub'),
        ),
    ]
