from django.db import models
from users.models import User
import uuid


class Project(models.Model):
    """
    Modèle pour gérer les projets créés par les utilisateurs.
    Seul l'auteur (créateur) peut modifier ou supprimer son projet.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(
        max_length=50,
        choices=[("Backend", "Backend"),
                 ("Frontend", "Frontend"),
                 ("IOS", "IOS"),
                 ("Android", "Android")]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    contributors = models.ManyToManyField(
        User, 
        through='Contributor',
        related_name="contributed_projects",
        blank=True
    )
    
    def __str__(self):
        return self.title
    
    
class Issue(models.Model):
    """
    Modèle pour gérer les tickets d'incidents liés à un projet.
    Seul l'auteur peut modifier ou supprimer son issue.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("To Do", "To Do"),
                 ("In Progress", "In Progress"),
                 ("Done", "Done")],
        default="To Do"
    )
    priority = models.CharField(
        max_length=10,
        choices=[("Low", "Low"),
                 ("Medium", "Medium"),
                 ("High", "High")],
        default="Medium"
    )
    tag = models.CharField(
        max_length=10,
        choices=[("Bug", "Bug"),
                 ("Feature", "Feature"),
                 ("Task", "Task")],
        default="Task"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issues")
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_issues")
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    
class Comment(models.Model):
    """
    Modèle pour gérer les commentaires liés a un ticket.
    Seul l'auteur peut modifier ou supprimer son commentaire.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"
    
    
class Contributor(models.Model):
    """
    Modèle qui définit les utilisateurs ayant accès à un projet.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contributions")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contributor_set")
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'project')
        
    def __str__(self):
        return f"{self.user.username} - {self.project.title}"
