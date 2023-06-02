from dataclasses import fields
from django.contrib import admin
from django.forms import TextInput, Textarea
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.text import Truncator
from .models import Utilisateur, DoleanceElu, DoleanceCse,\
    Panier, Produit, Commande, Clinique, Service, Personnel, registre_du_personnel,\
    Elu, Reponse, Personnel, SessionCse, Cse, ReponseElu, ReponseCse, Info, CategoryInfo 
from .forms import MonPersonnelCreationForm, MonEluCreationForm, MonUserChangeForm

# Register your models here.
  
# create a class for the admin-model integration
class TodoAdmin(admin.ModelAdmin):
  
    # add the fields of the model here
    list_display = ("title","description","completed")

#VARIABLE UTILE POUR LES 2 CLASSES SUIVANTES
lieu_travail = ('Lieu de travail', {'fields': ('la_clinique', 'le_service')})
class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    print(UserAdmin.fieldsets)
    print(type(UserAdmin.fieldsets[0]))
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('email', 'username', 'first_name', 'is_staff')
    ordering = ('username','-date_joined',)
    list_display = ('id', 'email', 'username', 'first_name',
                     'is_active', 'is_staff')

    fieldsets = ((None, {'fields': ('username', 'password')}), 
    ('Info Personelles', {'fields': ('civilite','first_name', 
    'last_name', 'email', 'phone')}), 
    lieu_travail,
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), 
    ('Dates importantes', {'fields': ('last_login', 'date_joined')}))
    

class PersonnelAdmin(UtilisateurAdmin):
    model: Personnel
    search_fields = ('email', 'username', 'first_name')
    list_filter = ('email', 'first_name', 'la_clinique', 'le_service')
    ordering = ('username','-date_joined')
    list_display = ('id', 'email', 'first_name',
                    'is_active', 'is_staff', 'la_clinique', 'le_service')
    
    add_fieldsets = (
        ('Données Personnelles', {
            #'classes': ('wide',), ou 'classes': ('collapse',),
            'fields': ('civilite',('username', 'first_name'), ('phone', 'email'), ('password1', 'password2'), 'apropos')}
         ),
        lieu_travail,
         ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active','groups')}),
    )

class EluAdmin(PersonnelAdmin):
    model = Elu
    add_fieldsets = (
        ('Données Personnelles', {
            'classes': ('wide',),
            'fields': ('civilite',('username', 'first_name'), ('phone', 'email'), ('password1', 'password2'), 'apropos')}
         ),
        lieu_travail,
        ('Données Syndicales', {
            'classes': ('wide',),
            'fields': ('syndicat','fonction', 'photo', 'message_aux_collègues', 'cse', 'disponible')}
         ),
         ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active','groups')}),
    )
    
class DoleanceEluAdmin(admin.ModelAdmin):
    # Personnalisation de l'affichage et de la gestion dans la page admin
    list_display = ('emeteur', 'apercu_contenu', 'objet', 'destinataire')
    list_filter = ('objet', 'emeteur', 'recepteur')
    date_hierarchy = 'date'
    ordering = ('date', )

    def destinataire(self,obj):
        return Elu.objects.get(pk=obj.recepteur)

    # Colonnes personnalisées
    def apercu_contenu(self, doleance):
      """
      Retourne les 40 premiers caractères du contenu de la doléance,
      suivi de points de suspension si le texte est plus long.

      On pourrait le coder nous même, mais Django fournit déjà la
      fonction qui le fait pour nous !
      """
      return Truncator(doleance.contenu).chars(40, truncate='...')
    # En-tête de notre colonne
    apercu_contenu.short_description = 'Aperçu du contenu'

    # Configuration du formulaire d'édition
    # Amélioration de l'affichage dans la page admin
    fieldsets = (
       # Fieldset 1 : meta-info (titre, membre…)
       ('Général', {
         'classes': ['collapse', ], # en dehors de la classe css collapse, il existe aussi wide et extrapretty
         'fields': ('emeteur', 'recepteur', 'objet',  'date') # essayer de rajouter le user ici
      }),
      # Fieldset 2 : contenu de l'article
      ('Contenu de la question', {
         # 'description': 'Question posée :',
         'fields': ('contenu',)
      }),
    )


class DoleanceCseAdmin(admin.ModelAdmin):
    # Personnalisation de l'affichage et de la gestion dans la page admin
    list_display = ('emeteur', 'objet', 'apercu_contenu', 'session', 'retenue')
    list_filter = ('emeteur', 'session', 'retenue')
    date_hierarchy = 'date'
    ordering = ('date', )
    search_fields = ('nom', 'prénom')

    def nom(self,obj):
        return obj
        # return Personnel.objects.get(nom=obj.personnel.nom).nom

    # Colonnes personnalisées
    def apercu_contenu(self, doleance):
      """
      Retourne les 40 premiers caractères du contenu de la doléance,
      suivi de points de suspension si le texte est plus long.

      On pourrait le coder nous même, mais Django fournit déjà la
      fonction qui le fait pour nous !
      """
      return Truncator(doleance.contenu).chars(40, truncate='...')
    # En-tête de notre colonne
    apercu_contenu.short_description = 'Aperçu du contenu'

    # Configuration du formulaire d'édition
    # Amélioration de l'affichage dans la page admin
    fieldsets = (
       # Fieldset 1 : meta-info (titre, membre…)
       ('Général', {
         'classes': ['collapse', ], # en dehors de la classe css collapse, il existe aussi wide et extrapretty
         'fields': ('emeteur', 'objet',  'date', 'session','recepteur_doleance') # essayer de rajouter le user ici
      }),
      # Fieldset 2 : contenu de l'article
      ('Contenu de la question', {
         # 'description': 'Question posée :',
         'fields': ('contenu', 'retenue')
      }),
    )


class PanierAdmin(admin.ModelAdmin): # Personnalisation de l'affichage et de la gestion dans la page admin
    list_display = ('id', 'commanditaire', 'total', 'lieu_retrait', 'date_retrait', 'date')
    list_filter = ('id', 'lieu_retrait', 'commanditaire')
    date_hierarchy = 'date'
    ordering = ('date', )
    search_fields  = ('valeur_totale',)

    def prix_adulte(self, obj):
        return str(obj.produit.prix_adulte)+' €'

    def prix_enfant(self, obj):
        return str(obj.produit.prix_enfant)+' €'


class ProduitAdmin(admin.ModelAdmin): # Personnalisation de l'affichage et de la gestion dans la page admin
    list_display = ('id','nom', 'prix_adulte', 'prix_enfant', 'disponible', 'photo')
    list_filter = ('nom','disponible')
    ordering = ('nom', )
    search_fields = ('nom',)

class CommandeAdmin(admin.ModelAdmin): # Personnalisation de l'affichage et de la gestion dans la page admin
    list_display = ('id', 'produit', 'billet_adulte', 'billet_enfant', 'sous_total')
    list_filter = ('produit',)
    ordering = ('id', )
    search_fields = ('produit',)


class CliniqueAdmin(admin.ModelAdmin):
    # list_display = ('nom_clinique', 'les_services')
    list_display = ('id','nom_clinique', 'adresse')
    list_filter = ('nom_clinique', 'adresse')
    ordering = ('nom_clinique',)
    search_fields = ('nom_clinique',)

    # def les_services(self, obj):
    #    return "\n".join([a.nom_service for a in obj.service.all()])


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('nom_service', 'lieu')
    list_filter = ('nom_service', )
    ordering = ('nom_service',)
    search_fields = ('nom_service', 'lieu')

    def lieu(self, obj):
       return obj.clinique.adresse


class RegistreDuPersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'clinique', 'service' , 'syndicat')
    list_filter = ('nom', 'prenom', 'civilite', 'syndicat')
    ordering = ('nom',)
    search_fields = ('nom', 'prenom')

class ReponseAdmin(admin.ModelAdmin):
    list_display = ('éméteur_question', 'objet', 'contenu', 'éméteur_réponse')
    list_filter = ('doleance', 'objet')
    ordering = ('doleance',)
    search_fields = ('doleance', 'objet')

    def éméteur_question(self,obj):
        pass
        #return Personnel.objects.get(pk=obj.recepteur)


class ReponseEluAdmin(ReponseAdmin):

    def éméteur_réponse(self,obj):
        pass
        #return Elu.objects.get(pk=obj.emeteur)


class ReponseCseAdmin(ReponseAdmin):

    def éméteur_réponse(self,obj):
        pass
        #return obj.emeteur


class SessionCseAdmin(admin.ModelAdmin):
    list_display = ('mois', 'date_debut', 'date_fin')
    list_filter = ('mois', )


class CseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'siege')
    list_filter = ('nom', )


# Changer l'entête de la page d'administration par defaut retirer cette ligne pour le texte par défaut
admin.site.site_header = "Page d'administration"

# Enregistrer les models
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Elu, EluAdmin)
admin.site.register(DoleanceElu, DoleanceEluAdmin)
admin.site.register(DoleanceCse, DoleanceCseAdmin)
admin.site.register(Panier, PanierAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Clinique, CliniqueAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(registre_du_personnel, RegistreDuPersonnelAdmin)
admin.site.register(SessionCse, SessionCseAdmin)
admin.site.register(Cse, CseAdmin)
# admin.site.register(Reponse, ReponseAdmin)
admin.site.register(ReponseElu, ReponseEluAdmin)
admin.site.register(ReponseCse, ReponseCseAdmin)

@admin.register(Info)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('titre', 'id', 'status', 'slogan', 'auteur', )
    prepopulated_fields = {'slogan': ('titre',), }

admin.site.register(CategoryInfo)
