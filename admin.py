from django.contrib import admin
from .models import Forme, ProcessRecipe, Recipe, Ingredient, Famille, Contraintes, IngredientRecipe, IngredientTest, FamilleTest, CookingRecipe#, ContraintesRecipe, ContraintesRecipe,
# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Forme)
admin.site.register(Famille)
admin.site.register(Contraintes)
admin.site.register(IngredientTest)
admin.site.register(FamilleTest)
#admin.site.register(Recipe)

class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    fk_name = "recipe"

class ProcessInline(admin.TabularInline):
    model = ProcessRecipe
    fk_name = "recipe"
    
    
class CookingInline(admin.TabularInline):
    model = CookingRecipe
    fk_name = "recipe"
    
    
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ProcessInline, CookingInline]