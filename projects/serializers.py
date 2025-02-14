from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor

# Serializer minimal pour l'affichage en liste
class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'affichage simplifié des projets.
    
    Permet d'afficher les informations essentielles d'un projet dans une liste.
    """
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Project
        # Champs essentiels à afficher dans une liste de projets
        fields = ('id', 'title', 'type', 'author')

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour les projets.
    
    Fournit une représentation complète d'un projet incluant toutes ses informations,
    ainsi que la liste des contributeurs. Le champ 'author' est en lecture seule et
    représente le nom d'utilisateur de l'auteur.
    """
    author = serializers.ReadOnlyField(source='author.username')
    contributors = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('author', 'created_time')
        
    def get_contributors(self, obj):
        """
        Retourne une liste contenant l'id et le nom d'utilisateur des contributeurs du projet.
        
        :param obj: Instance de Project
        :return: Liste de dictionnaires avec les clés 'id' et 'username'
        """
        return [{"id": user.id, "username": user.username} for user in obj.contributors.all()]
        
        
class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour les tickets (issues) d'un projet.
    
    Ce serializer gère la représentation des tickets avec le champ 'author' en lecture seule.
    """
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('author', 'created_time')
        
        
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer pour les commentaires associés aux tickets (issues).
    
    Le champ 'author' est en lecture seule et représente le nom d'utilisateur de
    l'auteur du commentaire.
    """
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'created_time')
  
        
class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour la gestion des contributeurs.
    
    Permet de représenter l'association entre un utilisateur et un projet.
    """
    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ('created_time',)