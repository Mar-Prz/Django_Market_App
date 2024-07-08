from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model): #this is our database model
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',) #specifies that the results should be ordered by the 'name' field in ascending order
        verbose_name_plural = 'Categories' #this changes the name from Categorys to Categories in our admin interface

    def __str__(self): #this makes the categories show their actual names so in this case clothes,furniture and toys and not category 1, category 2 etc
            return self.name #returns name from the Category class

class Item(models.Model):
     category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE) # Field Type (ForeignKey): This specifies that each instance of your model is related to a single instance of the Category model, setting up a many-to-one relationship.
     #First Argument (Category): This is the model with which you are creating the relationship. The Category model would typically be another model you've defined in your Django app that represents different categories.
     #related_name='items': This argument specifies the name to use for the reverse relation from the Category model back to your model. If you have a Category instance c, you can access all associated instances of your model by using c.items.
     #on_delete=models.CASCADE when a Category is deleted all associated instances of the model linked to that Category will be deleted
     name = models.CharField(max_length=255)
     description = models.TextField(blank=True, null=True) #blank and null are true in case the user doesn't want to provide a description for the project
     price = models.FloatField() #price will be a floating point number
     image = models.ImageField(upload_to='item_images', blank=True, null=True) #images will be uploaded to item_images and django will create this folder if we don't have it, blan is true and null is true in case the user doesn't want to provide an image
     is_sold = models.BooleanField(default=False) #indicates whether an item is sold with a default value of False
     created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE) #ForeignKey specifies that each instance of the model is related to a single instance of the User Model
     # User is the model which we are creating the relationship, here it is djangos built in user model
     # related_name='items': This is an optional argument that specifies the name to use for the reverse relation from the User model back to your model. If you have a User instance u, you can access all associated instances of your model by u.items.
     # on_delete=models.CASCADE tells django to delete everything when a User is deleted
     created_at = models.DateTimeField(auto_now_add=True) #this field automatically sets the date and time when a new record is created

     def __str__(self):
          return self.name