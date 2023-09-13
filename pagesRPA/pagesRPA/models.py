from django.db import models
#from django_admin_json_editor import JSONEditorWidget
#from django.contrib.postgres.fields import JSONField
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="项目代号")
    descript = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pages')
    url = models.URLField(blank=True, null=True)
    xpath = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    '''
    def get_absolute_url(self):
        return reverse('page_detail', args=[str(self.id)])
    '''
'''
class ElementType(models.Model):
    name = models.CharField(max_length=100)
    descript = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
'''

class Element(models.Model):
    ELEMENT_TYPE_CHOICES = (
        ('link', 'Link'),
        ('input', 'Input'),
        ('div', 'Div'),
        ('button', 'Button'),
        ('dd', 'Dd'),
        ('url', 'Goto'),
    )
    
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='elements')
    element_type = models.CharField(max_length=50, choices=ELEMENT_TYPE_CHOICES)
    descript = models.CharField(max_length=255, blank=True, null=True)
    xpath = models.TextField(blank=True, null=True)
    offset = models.IntegerField(default=0) 
    sequence = models.IntegerField() 

    title = models.CharField(max_length=200,blank=True, null=True)
    id_name = models.CharField(max_length=200,blank=True, null=True)
    name = models.CharField(max_length=200,blank=True, null=True)
    class_name = models.CharField(max_length=200,blank=True, null=True)
    text = models.CharField(max_length=200,blank=True, null=True)
    mark = models.CharField(max_length=100, unique=True)

    before_delay = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    after_delay = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    is_actived= models.BooleanField(default=True)
    check = models.BooleanField(default=False)
    #attributes = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.element_type} ({self.descript})"

    class Meta:
        verbose_name = 'Element'
        verbose_name_plural = 'Elements'
        ordering = ('id',)

        permissions = [
            ('duplicate_selected', 'Can copy element'),
            ('swap_sequence', 'Can swap element sequence'),
        ]
'''
class Action(models.Model):
    
    ACTION_TYPE_CHOICES = (
        ('click', 'Click'),
        ('type', 'Type Text'),
    )

    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='actions')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPE_CHOICES)
    value = models.CharField(max_length=255, blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True)


    def __str__(self):
        return f"{self.action_type} ({self.value})"

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'


class Condition(models.Model):
    CONDITION_TYPE_CHOICES = (
        ('equals', 'Equals'),
        ('contains', 'Contains'),
        ('startswith', 'Starts With'),
        ('endswith', 'Ends With'),
        ('matches', 'Matches'),
    )

    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name='conditions')
    condition_type = models.CharField(max_length=50, choices=CONDITION_TYPE_CHOICES)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.condition_type} ({self.value})"

    class Meta:
        verbose_name = 'Condition'
        verbose_name_plural = 'Conditions'
'''