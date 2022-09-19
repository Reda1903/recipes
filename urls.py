from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="recipe-home"),
    
    path('recettes/', views.recipes_view, name="recettes-recipe"),
    path('recettesadmin/', views.admin_recipe , name="recettes-recipe-admin"),
    path('recettesutilisateur/', views.admin_recipe , name="recettes-recipe-utilisateur"),
    
    path('recettes/<int:pk>', views.RecipeDetailView.as_view(), name="recettes-detail"),
    path('recettes/create', views.RecipeCreateView.as_view(), name="recettes-create"),
    #path('recipe/<int:pk>/update', views.RecipeUpdateView.as_view(), name="recettes-update"),
    path('recipe/<int:pk>/update', views.update_recipe2, name="recettes-update"),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name="recettes-delete"),

    #path('recipe/user/<int:pk>/delete', views.RecipeDeleteView2.as_view(), name="recettes-delete-user"),
    #path('recipe/<int:pk>/delete', views.RecipeDeleteViewAdmin, name="recettes-delete-admin"),
    
    #path('ingredients/', views.IngredientListView.as_view(), name="ingredients-recipe"),
    path('ingredients/', views.Ingredient_view , name="ingredients-recipe"),
    path('ingredients/<int:pk>', views.IngredientDetailView.as_view(), name="ingredients-detail"),
    path('ingredients/create', views.IngredientCreateView.as_view(), name="ingredients-create"),
    path('ingredients/<int:pk>/update', views.IngredientUpdateView.as_view(), name="ingredients-update"),
    path('ingredients/<int:pk>/delete', views.IngredientDeleteView.as_view(), name="ingredients-delete"),
    
    
    path('familles/', views.Famille_view, name="familles-recipe"),
    path('familles/<int:pk>', views.FamilleDetailView.as_view(), name="familles-detail"),
    path('familles/create', views.FamilleCreateView.as_view(), name="familles-create"),
    path('familles/<int:pk>/update', views.FamilleUpdateView.as_view(), name="familles-update"),
    path('familles/<int:pk>/delete', views.FamilleDeleteView.as_view(), name="familles-delete"),
    path('familles-ingredients/<int:pk>', views.Famille_ingredients, name="famille-ingredients"),
    
    path('ingredients/', views.ingredients, name="ingredients-recipe"),
    path('familles/', views.familles, name="familles-recipe"),

    path('export/', views.export_to_csv, name="export_to_csv"),

    path('create/', views.create_recipe2, name="create_recipe"),
    path('create_process/<int:pk>', views.create_process, name="create_recipe_process"),
    path('update_process/<int:pk>', views.update_process, name="update_recipe_process"),


    path('recipe/testCascade', views.ingredient_create_view, name="test_cascade"),

    #path('pdf/<int:pk>', views.GeneratePdf.as_view(), name="pdf_recipe"),
    path('pdf/<int:pk>', views.generatePdf, name="pdf_recipe"),

    path('ajax/load-ingredients/', views.load_ingredient, name='ajax_load_ingredient'),
    path('ajax/load-formes/', views.load_forme, name='ajax_load_forme'),
    
]
