from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor, User


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'affichage simplifié des projets.

    Permet d'afficher les informations essentielles d'un projet dans une liste.
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Project
        fields = ("id", "title", "type", "author")


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer complet pour les projets.

    Fournit une représentation complète d'un projet incluant toutes ses informations,
    ainsi que la liste des contributeurs. Le champ 'author' est en lecture seule et
    représente le nom d'utilisateur de l'auteur.
    """

    author = serializers.ReadOnlyField(source="author.username")
    contributors = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("author", "created_time")

    def get_contributors(self, obj):
        """
        Retourne une liste contenant l'id et le nom d'utilisateur des contributeurs du projet.

        :param obj: Instance de Project
        :return: Liste de dictionnaires avec les clés 'id' et 'username'
        """
        return [
            {"id": user.id, "username": user.username}
            for user in obj.contributors.all()
        ]


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour les tickets (issues) d'un projet.

    Ce serializer gère la représentation des tickets avec le champ 'author' en lecture seule
    et le champ 'assignee' en utilisant le username.
    """

    author = serializers.ReadOnlyField(source="author.username")
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ("author", "created_time")

    def validate(self, data):
        """
        Valide que si un assigné est fourni, cet utilisateur fait bien partie des contributeurs du projet.
        """
        assignee = data.get("assignee")
        if assignee is not None:
            project = data.get("project")
            if project is None:
                raise serializers.ValidationError(
                    "Le champ 'project' doit être renseigné pour l'assignation."
                )
            # Vérifier que l'utilisateur assigné est bien contributeur du projet
            if not Contributor.objects.filter(project=project, user=assignee).exists():
                raise serializers.ValidationError(
                    "L'utilisateur assigné doit être contributeur du projet."
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer pour les commentaires associés aux tickets (issues).

    Le champ 'author' est en lecture seule et représente le nom d'utilisateur de
    l'auteur du commentaire.
    """

    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("author", "created_time")


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour la gestion des contributeurs.

    Permet de représenter l'association entre un utilisateur et un projet.
    Ici, on utilise SlugRelatedField pour pouvoir ajouter un contributeur en fournissant son nom d'utilisateur (username)
    plutôt que son ID.
    """

    # Ce champ permet de convertir automatiquement le username reçu en instance User et vice-versa.
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Contributor
        fields = "__all__"
        read_only_fields = ("created_time",)
