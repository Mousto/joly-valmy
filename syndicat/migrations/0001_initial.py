# Generated by Django 4.0.6 on 2023-03-03 08:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='adresse mail')),
                ('user_name', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('apropos', models.TextField(blank=True, max_length=500)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_categorie', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Clinique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_clinique', models.CharField(max_length=42)),
                ('adresse', models.CharField(max_length=42)),
            ],
            options={
                'verbose_name': 'clinique',
            },
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billet_adulte', models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('billet_enfant', models.PositiveIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('sous_total', models.FloatField(default=0)),
            ],
            options={
                'verbose_name': 'commande',
            },
        ),
        migrations.CreateModel(
            name='Cse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=60)),
                ('siege', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Doleance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet', models.CharField(max_length=60)),
                ('contenu', models.TextField()),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date de demande')),
                ('retenue', models.BooleanField(default=False)),
                ('emeteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emeteur_doleances', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Doléance(s) employé',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=42)),
                ('prix_adulte', models.FloatField(default=0)),
                ('prix_enfant', models.FloatField(default=0)),
                ('disponible', models.BooleanField()),
                ('photo', models.ImageField(null=True, upload_to='img-produits/')),
            ],
            options={
                'verbose_name': 'produit',
            },
        ),
        migrations.CreateModel(
            name='registre_du_personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=42)),
                ('prenom', models.CharField(max_length=42)),
                ('clinique', models.CharField(default='', max_length=42)),
                ('service', models.CharField(default='', max_length=42)),
                ('civilite', models.CharField(default='', max_length=42)),
                ('syndicat', models.CharField(default='', max_length=42)),
            ],
            options={
                'verbose_name': 'Registre du personnel',
                'ordering': ['nom'],
            },
        ),
        migrations.CreateModel(
            name='Reponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet', models.CharField(max_length=42)),
                ('contenu', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de réponse')),
                ('recepteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepteur_reponses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Réponse élu',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='SessionCse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.CharField(max_length=60)),
                ('date_debut', models.DateField(default=django.utils.timezone.now, verbose_name='Date_début_séssion')),
                ('date_fin', models.DateField(default=django.utils.timezone.now, verbose_name='Date_fin_séssion')),
            ],
        ),
        migrations.CreateModel(
            name='DoleanceCse',
            fields=[
                ('doleance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='syndicat.doleance')),
                ('recepteur_doleance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepteur_doleances_cse', to='syndicat.cse')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_doleances_cse', to='syndicat.sessioncse')),
            ],
            bases=('syndicat.doleance',),
        ),
        migrations.CreateModel(
            name='DoleanceElu',
            fields=[
                ('doleance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='syndicat.doleance')),
            ],
            bases=('syndicat.doleance',),
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('utilisateur_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('civilite', models.CharField(max_length=12)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('la_clinique', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='clinique', to='syndicat.clinique')),
            ],
            options={
                'abstract': False,
            },
            bases=('syndicat.utilisateur',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_service', models.CharField(max_length=42)),
                ('clinique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='syndicat.clinique')),
            ],
            options={
                'verbose_name': 'service',
            },
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur_totale', models.FloatField(default=0)),
                ('date_retrait', models.DateField(null=True)),
                ('lieu_retrait', models.CharField(choices=[('Talant', 'Bénigne joly'), ('Valmy', 'SSR Valmy')], default='Talant', max_length=60)),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Date de commande')),
                ('commandes', models.ManyToManyField(to='syndicat.commande')),
                ('commanditaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commanditaire', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produit', to='syndicat.produit'),
        ),
        migrations.CreateModel(
            name='Elu',
            fields=[
                ('personnel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='syndicat.personnel')),
                ('syndicat', models.CharField(default='', max_length=60)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('fonction', models.CharField(max_length=120)),
                ('message_aux_collègues', models.TextField(blank=True, null=True)),
                ('disponible', models.BooleanField(default=False)),
                ('cse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cse', to='syndicat.cse')),
            ],
            options={
                'verbose_name': 'élu',
            },
            bases=('syndicat.personnel',),
        ),
        migrations.CreateModel(
            name='ReponseCse',
            fields=[
                ('reponse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='syndicat.reponse')),
                ('doleance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_cse', to='syndicat.doleancecse')),
                ('emeteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emetteur_reponse_cse', to='syndicat.cse')),
            ],
            bases=('syndicat.reponse',),
        ),
        migrations.AddField(
            model_name='personnel',
            name='le_service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='service', to='syndicat.service'),
        ),
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=250)),
                ('extrait', models.TextField(null=True)),
                ('contenu', models.TextField()),
                ('slogan', models.SlugField(max_length=250, unique_for_date='publiée')),
                ('publiée', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('brouillon', 'Brouillon'), ('publiée', 'Publiée')], default='publiée', max_length=10)),
                ('categorie', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='syndicat.categoryinfo')),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='infos', to='syndicat.personnel')),
            ],
            options={
                'ordering': ('-publiée',),
            },
        ),
        migrations.CreateModel(
            name='ReponseElu',
            fields=[
                ('reponse_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='syndicat.reponse')),
                ('doleance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_elu', to='syndicat.doleanceelu')),
                ('emeteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emetteur_reponse_elu', to='syndicat.elu')),
            ],
            bases=('syndicat.reponse',),
        ),
        migrations.AddField(
            model_name='doleanceelu',
            name='recepteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recepteur_doleances_elu', to='syndicat.elu'),
        ),
    ]
