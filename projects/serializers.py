from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    contributors = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
        
    def get_contributors(self, obj):
        """Retourne une liste avec les noms des contributeurs au lieu des IDs."""
        return [{"id": user.id, "username": user.username} for user in obj.contributors.all()]
        
        
class IssueSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Issue
        fields = '__all__'
        
        
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = '__all__'
  
        
class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'