from email.policy import default
#from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.http import Http404


# Create your models here.

class CategoryInfo(models.Model):
    nom_categorie = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_categorie


class Info(models.Model):

    class InfoObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='publiée')


    PUBLICATION = 'publiée'
    options =(
        ('brouillon', 'Brouillon'),
        (PUBLICATION, 'Publiée')
    )

    categorie = models.ForeignKey(CategoryInfo, on_delete=models.CASCADE, default=1)
    titre = models.CharField(max_length=250)
    extrait = models.TextField(null=True)
    contenu = models.TextField()
    slogan = models.SlugField(max_length=250, unique_for_date=PUBLICATION)
    publiée = models.DateTimeField(default=timezone.now)
    auteur = models.ForeignKey('Personnel', on_delete=models.CASCADE, related_name='infos')
    status = models.CharField(max_length=10, choices=options, default=PUBLICATION)
    objects = models.Manager() # Manager par defaut
    infoObjects = InfoObjects() # Manager personnalisé

    class Meta:
        ordering = ('-publiée',)

    def __str__(self):
        return self.titre

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('last_name', '')

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if  not other_fields.get('last_name') :
            return ''

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    civilite = models.CharField(max_length=12, blank=False)
    email = models.EmailField(_('adresse mail'), unique=True)
    username = models.CharField(max_length=150, unique=False)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    apropos = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.civilite} {self.username} {self.first_name}"

    
    def get_object(self, pk):
        try:
            return Utilisateur.objects.get(pk=pk)
        except Utilisateur.DoesNotExist:
            raise Http404
    
    

class Personnel(Utilisateur):
    phone = PhoneNumberField(null=False, blank=False, unique=False)
    la_clinique = models.ForeignKey('Clinique', on_delete=models.CASCADE, null=False, default=1, related_name='clinique')
    le_service = models.ForeignKey('Service', on_delete=models.CASCADE, null=False, default=1, related_name='service')


    def get_clinique(self):
        return self.la_clinique.nom_clinique

    def get_service(self):
        return self.le_service.nom_service

    def username(self):
        return self.user_name
    

""" class Personnel(AbstractUser):
    # Mes ajouts de champs
    civilite = models.CharField(max_length=12)
    phone = PhoneNumberField(null=False, blank=False, unique=False)
    la_clinique = models.ForeignKey('Clinique', on_delete=models.CASCADE, null=True, related_name='clinique')
    le_service = models.ForeignKey('Service', on_delete=models.CASCADE, null=True, related_name='service')

    class Meta:
        verbose_name = "Personnel"
    
    def __str__(self):
        
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que
        nous traiterons plus tard dans l'administration
        
        return self.get_full_name() # f"{self.user.last_name} {self.user.first_name} "
    
    def get_clinique(self):
        return self.la_clinique.nom_clinique

    def get_service(self):
        return self.le_service.nom_service """


class Elu(Personnel):
    syndicat = models.CharField(max_length=60, default='')
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    fonction = models.CharField(max_length=120)
    message_aux_collègues = models.TextField(null=True, blank=True)
    cse = models.ForeignKey('Cse',on_delete=models.CASCADE, related_name="cse", null=True)
    disponible = models.BooleanField(default=False,)

    class Meta:
        verbose_name = "élu"

    @property
    def photo_profil_url(self):
        if self.photo.url is not None:
            return self.photo.url
        else:
            if self.civilite == 'Madame':
                print('madame###################################')
                return '/media/photos/defaut_femme.jpg'
            else:
                return '/media/photos/defaut_photo_homme.png'

    def mon_type(self):
        """ Utile pour ajax dans profil.js pour la maj du profil dans l'onglet 'Mon compte' """
        return str(type(self)).split('.')[2].replace("'", '').replace('>', '')

class registre_du_personnel(models.Model):
    nom = models.CharField(max_length=42)
    prenom = models.CharField(max_length=42)
    clinique = models.CharField(max_length=42, default='')
    service = models.CharField(max_length=42, default='')
    civilite = models.CharField(max_length=42, default='')
    syndicat = models.CharField(max_length=42, default='')

    class Meta:
        verbose_name = "Registre du personnel"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} {self.prenom} "


class Doleance(models.Model):
    emeteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='emeteur_doleances')
    objet = models.CharField(max_length=60)
    contenu = models.TextField()
    date = models.DateField(default=timezone.now,
                                verbose_name="Date de demande")
    retenue = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Doléance(s) employé"
        ordering = ['date']

    def __str__(self):
        """
        Cette méthode nous permet de reconnaître facilement les différents objets que
        nous traitons
        """
        return f"{self.emeteur} -- Objet : {self.objet} --"

    def get_object(self, pk):
        try:
            return Doleance.objects.get(pk=pk)
        except Doleance.DoesNotExist:
            raise Http404


class SessionCse(models.Model):
    mois = models.CharField(max_length=60)
    date_debut = models.DateField(default=timezone.now, verbose_name="Date_début_séssion")
    date_fin = models.DateField(default=timezone.now, verbose_name="Date_fin_séssion")

    def __str__(self):
        """
        Cette méthode nous permet de reconnaître facilement les différents objets que
        nous traitons
        """
        return f"{'Séssion'} {self.mois}"


class DoleanceElu(Doleance):
    recepteur = models.ForeignKey(Elu, on_delete=models.CASCADE, related_name='recepteur_doleances_elu')

    def to_dict(self):
        les_mois_f = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE",
                      "NOVEMBRE", "DÉCEMBRE"]
        les_mois_a = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                      "November", "December"]
        le_mois = ""
        for m in range(len(les_mois_a)):
            if self.date.strftime("%B") == les_mois_a[m]:
                le_mois = les_mois_f[m]
        return {"emeteur": f"{self.emeteur}", "objet": self.objet, "contenu": self.contenu,
                "date": self.date.strftime("%d") + " " + le_mois + " " + self.date.strftime("%Y"),
                "recepteur": f"{self.recepteur}", "id": self.id }


class DoleanceCse(Doleance):
    session = models.ForeignKey(SessionCse, on_delete=models.CASCADE, related_name='session_doleances_cse')
    recepteur_doleance = models.ForeignKey('Cse', on_delete=models.CASCADE, related_name='recepteur_doleances_cse')

    def to_dict(self):
        les_mois_f = ["JANVIER", "FÉVRIER", "MARS", "AVRIL", "MAI", "JUIN", "JUILLET", "AOÛT", "SEPTEMBRE", "OCTOBRE",
                      "NOVEMBRE", "DÉCEMBRE"]
        les_mois_a = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                      "November", "December"]
        le_mois = ""
        for m in range(len(les_mois_a)):
            if self.date.strftime("%B") == les_mois_a[m]:
                le_mois = les_mois_f[m]
        return {"emeteur": f"{self.emeteur}", "objet": self.objet, "contenu": self.contenu,
                "date": self.date.strftime("%d") + " " + le_mois + " " + self.date.strftime("%Y"),
                "recepteur": f"{self.recepteur_doleance}", "id": self.id, 'session': f"{self.session}" },


class Reponse(models.Model):
    recepteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='recepteur_reponses')
    objet = models.CharField(max_length=42)
    contenu = models.TextField()
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de réponse")

    class Meta:
        verbose_name = "Réponse élu"
        ordering = ['date']

    def __str__(self):
        """
        Cette méthode nous permet de reconnaître facilement les différents objets que
        nous traitons
        """
        return self.objet
    
    def get_object(self, pk):
        try:
            return Reponse.objects.get(pk=pk)
        except Reponse.DoesNotExist:
            raise Http404

class ReponseElu(Reponse):
    doleance = models.ForeignKey(DoleanceElu, on_delete=models.CASCADE, related_name='question_elu')
    emeteur = models.ForeignKey(Elu, on_delete=models.CASCADE, related_name='emetteur_reponse_elu')

    
    def get_object(self, pk):
        try:
            return ReponseElu.objects.get(pk=pk)
        except ReponseElu.DoesNotExist:
            raise Http404


class ReponseCse(Reponse):
    doleance = models.ForeignKey(DoleanceCse, on_delete=models.CASCADE, related_name='question_cse')
    emeteur = models.ForeignKey('Cse', on_delete=models.CASCADE, related_name='emetteur_reponse_cse')

    def get_object(self, pk):
        try:
            return ReponseCse.objects.get(pk=pk)
        except ReponseCse.DoesNotExist:
            raise Http404

class Produit(models.Model):

    # Ne renvoie que les produits disponibles
    # class ProduitDispo(models.Manager):
    #     def get_queryset(self):
    #         return super().get_queryset().filter(disponible=True)

    nom = models.CharField(max_length=42, blank=False, null=False)
    prix_adulte = models.FloatField(default=0)
    prix_enfant = models.FloatField(default=0)
    disponible = models.BooleanField()
    photo = models.ImageField(upload_to='img-produits/', null=False, default='')
    # billet_adulte = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], blank=True)
    # billet_enfant = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], blank=True)
    # sous_total = models.FloatField(default=0)

    # objects = models.Manager # default manager
    # produitdispo = ProduitDispo()

    class Meta:
        verbose_name = "produit"

    def __str__(self):
        return self.nom
    
    def get_object(self, pk):
        try:
            return Produit.objects.get(pk=pk)
        except Produit.DoesNotExist:
            raise Http404


class Commande(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='produit')
    billet_adulte = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], blank=True)
    billet_enfant = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)], blank=True)
    sous_total = models.FloatField(default=0)

    class Meta:
        verbose_name = "commande"

    def __str__(self):
        return f'Commande {self.produit}'
    
    def get_object(self, pk):
        try:
            return Commande.objects.get(pk=pk)
        except Commande.DoesNotExist:
            raise Http404
    
    def getSousTotal(self):
        return (self.produit.prix_adulte * self.billet_adulte) + (self.produit.prix_enfant * self.billet_enfant)

class Panier(models.Model):

    class PanierObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(commanditaire=self.commanditaire)

    choix_clinique = (
        ('Talant', 'Bénigne joly'),
        ('Valmy', 'SSR Valmy'),
    )
    commandes = models.ManyToManyField(Commande)
    # billet_adulte = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    # billet_enfant = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    valeur_totale = models.FloatField(default=0)
    date_retrait = models.DateField(null=True)
    lieu_retrait = models.CharField(
        max_length=60,
        choices=choix_clinique,
        default='Talant',
    )
    date = models.DateField(default=timezone.now,
                            verbose_name="Date de commande")
    commanditaire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,
                                      related_name='commanditaire')  # La liaison OneToOne vers le modèle User

    #commande_honorée = False


    objects = models.Manager() # Manager par defaut
    infoObjects = PanierObjects() # Manager personnalisé


    def __str__(self):
        return f'Commande {self.commanditaire}'
        return str(self.produit)

    def total(self):
        return self.valeur_totale

    def get_object(self, pk):
        try:
            return Panier.objects.get(pk=pk)
        except Panier.DoesNotExist:
            raise Http404


class Service(models.Model):
    nom_service = models.CharField(max_length=42)
    clinique = models.ForeignKey('Clinique', on_delete=models.CASCADE, related_name='services')

    class Meta:
        verbose_name = "service"

    def __str__(self):
        return self.nom_service

    def get_object(self, pk):
        try:
            return Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            raise Http404


class Clinique(models.Model):
    nom_clinique = models.CharField(max_length=42)
    adresse = models.CharField(max_length=42)

    class Meta:
        verbose_name = "clinique"

    def __str__(self):
        return self.nom_clinique

    def get_object(self, pk):
        try:
            return Clinique.objects.get(pk=pk)
        except Clinique.DoesNotExist:
            raise Http404


class Cse(models.Model):
    nom = models.CharField(max_length=60)
    siege = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nom}"

    def get_object(self, pk):
        try:
            return Cse.objects.get(pk=pk)
        except Cse.DoesNotExist:
            raise Http404