from shutil import _ntuple_diskusage
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#from my_project.recipe.views import ingredients


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=500)
    #description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    #prep_time = models.DurationField()
    #cook_time = models.DurationField()
    #servings = models.IntegerField()


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recettes-detail", kwargs={"pk": self.pk})
    
     
    
class Famille(models.Model):
    
#    name = models.CharField(max_length=100,   unique=True)
    name = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("familles-detail", kwargs={"pk": self.pk})

class Forme(models.Model):
    name = models.CharField(max_length=500)
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="forme_famille", null=True)
    def __str__(self):
        return self.name
    
    #def get_absolute_url(self):
        #return reverse("familles-detail", kwargs={"pk": self.pk})
    
class Ingredient(models.Model):
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="famille_ingredient", null=True)
    forme = models.ForeignKey(Forme, on_delete=models.CASCADE, related_name="forme_ingredient", null=True, verbose_name='ingrédient')
    name = models.CharField(max_length=500, verbose_name='forme')
    energie_kJ = models.FloatField(null= True)
    energie_kcal = models.FloatField(null= True)
    sodium = models.FloatField(null= True)
    glucide = models.FloatField(null= True)
    proteins = models.FloatField(null= True)
    
    fibres = models.FloatField(null= True)
    eau = models.FloatField(null= True)
    lipide = models.FloatField(null= True)
    sucres = models.FloatField(null= True)
    fructose = models.FloatField(null= True)
    galactose = models.FloatField(null= True)
    glucose = models.FloatField(null= True)
    lactose = models.FloatField(null= True)
    maltose = models.FloatField(null= True)
    saccharose = models.FloatField(null= True)
    amidon = models.FloatField(null= True)

    fibresALimentraires = models.FloatField(null= True)
    polyols = models.FloatField(null= True)
    cendres = models.FloatField(null= True)
    alcool = models.FloatField(null= True)

    acidesOrganiques = models.FloatField(null= True)
    AGsatures = models.FloatField(null= True)
    AGmonoinsature = models.FloatField(null= True)
    AGpolyinsature = models.FloatField(null= True)
    AGbutyrique = models.FloatField(null= True)
    AGcaproique = models.FloatField(null= True)
    AGcaprylique = models.FloatField(null= True)
    AGcaprique = models.FloatField(null= True)
    AGlaurique = models.FloatField(null= True)
    AGmyristique = models.FloatField(null= True)
    AGpalmitique = models.FloatField(null= True)
    AGbstearique = models.FloatField(null= True)
    AGoleique = models.FloatField(null= True)
    AGlinoleique = models.FloatField(null= True)
    AGalphalinolenique = models.FloatField(null= True)

    AGarachidonique = models.FloatField(null= True)
    AGepa = models.FloatField(null= True)
    AGdha = models.FloatField(null = True)

    cholesterol = models.FloatField(null= True)
    selchlorure = models.FloatField(null= True)
    calcium = models.FloatField(null= True)
    chlorure = models.FloatField(null= True)
    cuivre = models.FloatField(null= True)
    fer = models.FloatField(null= True)
    iode = models.FloatField(null= True)
    magnesium = models.FloatField(null= True)
    manganese = models.FloatField(null= True)
    phosphore = models.FloatField(null= True)
    potassium = models.FloatField(null= True)
    selenium = models.FloatField(null= True)
    zinc = models.FloatField(null= True)

    retinol = models.FloatField(null= True)
    betaCarotene = models.FloatField(null= True)

    vitamineD = models.FloatField(null= True)
    vitamineE = models.FloatField(null= True)
    VitamineK1 = models.FloatField(null= True)
    vitamineK2 = models.FloatField(null= True)
    #Vitamine C
    vitamineB1 = models.FloatField(null= True)
    vitamineB2 = models.FloatField(null= True)
    VitamineB3 = models.FloatField(null= True)
    vitamineB5 = models.FloatField(null= True)
    vitamineB6 = models.FloatField(null= True)
    vitamineB9 = models.FloatField(null= True)

    #to chaine into vitamine minuscule
    VitamineB12 = models.FloatField(null= True)



    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("ingredients-detail", kwargs={"pk": self.pk})
    
class Contraintes(models.Model):
    famille_1 = models.ForeignKey(Famille, on_delete=models.CASCADE)
    seuil = models.FloatField()
    
class IngredientRecipe(models.Model): 
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE, related_name="ingredients_recipe_famille", null=True)
    forme = models.ForeignKey(Forme, on_delete=models.CASCADE, related_name="ingredients_recipe_forme", null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients_recipe")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="xyz", null=True)
    #ingredient = models.CharField(max_length=100)
    quantity = models.FloatField(null=True)
    
    
    def __str__(self):  
        return self.ingredient.name

class ProcessRecipe(models.Model): 
    step = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="process_recipe")

    #ingredient = models.CharField(max_length=100)
    
    
    def __str__(self):  
        return self.recipe.title


class CookingRecipe(models.Model): 
    step = models.CharField(max_length=100)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="cooking_recipe")

    #ingredient = models.CharField(max_length=100)
    
    
    def __str__(self):  
        return self.recipe.title


class WeigthRecipe(models.Model):
    unitaire = models.FloatField(default=13.5)
    cru = models.FloatField(default=13.5)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="weight_recipe")

    def __str__(self):  
        return self.recipe.title


class FamilleTest(models.Model):
    name = models.CharField(max_length=100)
       
    def __str__(self):  
        return self.name        

class IngredientTest(models.Model):
    name = models.CharField(max_length=100)
    famille = models.ForeignKey(FamilleTest, on_delete=models.CASCADE, related_name="famille_ingredient")  
    energie_kJ = models.FloatField(null= True)

    def __str__(self):  
        return self.name




'''    
class ContraintesRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_recette = models.ForeignKey(IngredientRecipe, on_delete=models.CASCADE)
    contraintes_recette = models.ForeignKey(Contraintes, on_delete=models.CASCADE)
    
    
    def __str__(self):  
        return self.name'''