from asyncore import read
from audioop import reverse
from multiprocessing import context
from time import timezone
from unicodedata import name
from urllib import request
#from turtle import clone, title
#from turtle import title
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
import requests  
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime
import csv 

from .process import html_to_pdf 

from . import models
from .forms import ProcessFormSet, RecipeForm, IngredientForm, IngredientFormSet, CookingForm, CookingFormSet, WeightFormSet

#from my_project import recipe

# Create your views here.
''' Objects transmitted into the context'''

recipes = [{
        'title' : 'burger',
        'description' : 'combine ingredients',
        'cook_time' : '30' 
    },{
        'title' : 'Pizza',
        'description' : 'combine ingredients',
        'cook_time' : '40' 
    },{
        'title' : 'Pizza',
        'description' : 'combine ingredients',
        'date_posted' : '50' }]

recipes = models.Recipe.objects.all()
ingredients_app = models.Ingredient.objects.all()
familles_app = models.Famille.objects.all()
contraintes = models.Contraintes.objects.all()
ingredients_recette = models.IngredientRecipe.objects.all()


#Creating a class based view
#class GeneratePdf(View):
 #    def get(self, request, pk, *args, **kwargs):
        #récuperer l'ID de la recette 
  #      print(pk)
        #génerer la page html de ses détails  
        # getting the template
   #     pdf = html_to_pdf('result.html')
         
         # rendering the template
    #    return HttpResponse(pdf, content_type='application/pdf')



''' Export ingredients as csv '''
def export_to_csv(request):
    ingredients = models.Ingredient.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ingredient_export.csv'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['Famille','Ingrédient', 'Forme', 'Energie. Règlement UE N° 1169/2011 (kJ/100 g)',
    'Energie, Règlement UE N° 1169/2011 (kcal/100 g)', 'Eau (g/100 g)',
    'Protéines, N x facteur de Jones (g/100 g)', 'Glucides (g/100 g)', 'Lipides (g/100 g)',
    'Sucres (g/100 g)', 'Fructose (g/100 g)', 'Galactose (g/100 g)', 'Glucose (g/100 g)', 
    'Lactose (g/100 g)', 'Maltose (g/100 g)', 'Saccharose (g/100 g)', 'Amidon (g/100 g)', 
    'Fibres alimentaires (g/100 g)', 'Polyols totaux (g/100 g)', 'Cendres (g/100 g)', 'Alcool (g/100 g)', 
    'Acides organiques (g/100 g)', 'AG saturés (g/100 g)', 'AG monoinsaturés (g/100 g)', 
    'AG polyinsaturés (g/100 g)', 'AG 4:0, butyrique (g/100 g)', 'AG 6:0, caproïque (g/100 g)',
    'AG 8:0, caprylique (g/100 g)', 'AG 10:0, caprique (g/100 g)', 'AG 12:0, laurique (g/100 g)',
    'AG 14:0, myristique (g/100 g)', 'AG 16:0, palmitique (g/100 g)', 'AG 18:0, stéarique (g/100 g)',
    'AG 18:1 9c (n-9), oléique (g/100 g)', 'AG 18:2 9c,12c (n-6), linoléique (g/100 g)', 
    'AG 18:3 c9,c12,c15 (n-3), alpha-linolénique (g/100 g)', 'AG 20:4 5c,8c,11c,14c (n-6), arachidonique (g/100 g)',
    'AG 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100 g)', 'AG 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100 g)',
    'Cholestérol (mg/100 g)', 'Sel chlorure de sodium (g/100 g)', 'Calcium (mg/100 g)', 'Chlorure (mg/100 g)',
    'Cuivre (mg/100 g)', 'Fer (mg/100 g)', 'Iode (µg/100 g)', 'Magnésium (mg/100 g)', 'Manganèse (mg/100 g)',
    'Phosphore (mg/100 g)', 'Potassium (mg/100 g)', 'Sélénium (µg/100 g)', 'Sodium (mg/100 g)', 'Zinc (mg/100 g)', 
    'Rétinol (µg/100 g)', 'Beta-Carotène (µg/100 g)', 'Vitamine D (µg/100 g)', 'Vitamine E (mg/100 g)',
    'Vitamine K1 (µg/100 g)', 'Vitamine K2 (µg/100 g)', 'Vitamine B1 ou Thiamine (mg/100 g)',
    'Vitamine B2 ou Riboflavine (mg/100 g)', 'Vitamine B3 ou PP ou Niacine (mg/100 g)', 'Vitamine B5 ou Acide pantothénique (mg/100 g)',
    'Vitamine B6 (mg/100 g)', 'Vitamine B9 ou Folates totaux (µg/100 g)', 'Vitamine B12 (µg/100 g)'])

    ingredient_fields = ingredients.values_list('famille', 'forme', 'name', 'energie_kJ',
    'energie_kcal', 'eau',
    'proteins', 'glucide', 'lipide',
    'sucres', 'fructose', 'galactose', 'glucose', 
    'lactose', 'maltose', 'saccharose', 'amidon', 
    'fibresALimentraires', 'polyols', 'cendres', 'alcool', 
    'acidesOrganiques', 'AGsatures', 'AGmonoinsature', 
    'AGpolyinsature', 'AGbutyrique', 'AGcaproique',
    'AGcaprylique', 'AGcaprique', 'AGlaurique',
    'AGmyristique', 'AGpalmitique', 'AGbstearique',
    'AGoleique', 'AGlinoleique', 
    'AGalphalinolenique', 'AGarachidonique',
    'AGepa', 'AGdha',
    'cholesterol', 'selchlorure', 'calcium', 'chlorure',
    'cuivre', 'fer', 'iode', 'magnesium', 'manganese',
    'phosphore', 'potassium', 'selenium', 'sodium', 'zinc', 
    'retinol', 'betaCarotene', 'vitamineD', 'vitamineE',
    'VitamineK1', 'vitamineK2', 'vitamineB1',
    'vitamineB2', 'VitamineB3', 'vitamineB5',
    'vitamineB6', 'vitamineB9', 'VitamineB12')

    for ingredient in ingredient_fields :
        ready = []
        ready.append(models.Famille.objects.get(id = ingredient[0]))
        ready.append(models.Forme.objects.get(id = ingredient[1]))
        ready.append(ingredient[2])
        for i in range(len(ingredient)):
            if i > 2 :
                ready.append(ingredient[i])
        writer.writerow(ready)
    return response


'''Function to generate PDFs'''   
def generatePdf(request, pk):        #récuperer l'ID de la recette 
    #print(pk)
    #génerer la page html de ses détails  
    # getting the template

    recipe = models.Recipe.objects.filter(id = pk)[0]

    def total_calorie() : 
        '''
        Calculer les totaux des différents attributs des ingrédients présents dans la recette. Les stocker dans un dicionnaire
        '''

        ingredients = models.IngredientRecipe.objects.filter(recipe = recipe)

    def total_calorie() : 
        '''
        Calculer les totaux des différents attributs des ingrédients présents dans la recette. Les stocker dans un dicionnaire
        '''

        ingredients = models.IngredientRecipe.objects.filter(recipe = recipe)
        quantite_total = 0

        total_calorique = 0 
        total_calorique_kcal = 0 
        total_glucide = 0
        total_sodium = 0
        total_sel = 0

        total_proteins = 0 
        total_fibres = 0 
        total_eau= 0
        total_lipide = 0

        total_sucres = 0
        total_fructose = 0 
        total_galactose = 0 
        total_glucose= 0
        total_lactose = 0
        total_maltose= 0 
        total_saccharose = 0 
        total_amidon= 0

        total_fibresAlimentaires = 0
        total_polyols= 0 
        total_cendres = 0 
        total_alcool= 0
        
        total_acidesOrganiques = 0
        total_AGsatures = 0 
        total_AGmonoinsature = 0 
        total_AGpolyinsature = 0
        total_AGbutyrique = 0
        total_AGcaproique = 0 
        total_AGcaprylique = 0 
        total_AGcaprique = 0

        total_AGlaurique = 0 
        total_AGmyristique = 0
        total_AGpalmitique = 0
        total_AGbstearique = 0 
        total_AGoleique = 0 
        
        total_AGlinoleique = 0 
        total_AGalphalinolenique = 0

        total_AGepa = 0
        total_AGdha = 0

        total_cholesterol = 0 
        total_selchlorure = 0
        total_calcium = 0 
        total_cuivre = 0
        total_fer = 0 
        total_iode = 0 
        total_magnesium = 0
        total_manganese = 0
        total_phosphore = 0
        total_potassium= 0 
        total_selenium = 0 
        total_zinc = 0
        total_retinol= 0
        total_betacarotene = 0

        total_vitamineD = 0
        total_vitamineE = 0 
        total_VitamineK1 = 0 
        total_vitamineK2 = 0
        total_vitamineB1 = 0
        total_vitamineB2 = 0 
        total_vitamineB3 = 0
        total_VitamineB5 = 0 
        total_vitamineB6 = 0
        total_VitamineB9 = 0 
        total_vitamineB12 = 0

        Total_eau_ajoutee = 0
        total_fibresAlimentaires = 0
        total_sels_ajoutes = 0
        total_sucres_ajoutes = 0

        Total_graisses_ajoutes = 0
        Total_fruitslegumineuse = 0

        quantite_total = 0.001
        if ingredients.__len__ == 0 :
            quantite_total = 1
            print(ingredients)
            print(" est vide")

        else :
            print(ingredients)
        for ingredient in ingredients : 

            if ingredient.ingredient.forme.name=='sels' :
                total_sels_ajoutes = total_sels_ajoutes + ingredient.quantity 

            if ingredient.ingredient.forme.name=='sucres, miels et assimilés' :
                total_sucres_ajoutes = total_sucres_ajoutes + ingredient.quantity 


            if ingredient.ingredient.forme.name =='eaux' :
                Total_eau_ajoutee = Total_eau_ajoutee + ingredient.quantity 


            if ingredient.ingredient.famille.name =='matières grasses' :
                Total_graisses_ajoutes = Total_graisses_ajoutes + ingredient.quantity 

            if ingredient.ingredient.famille.name =='fruits, légumes, légumineuses et oléagineux' :
                Total_fruitslegumineuse = Total_fruitslegumineuse + ingredient.quantity 

 
            if isinstance(ingredient.ingredient.energie_kJ, float):
                total_calorique  = total_calorique + ingredient.quantity * (ingredient.ingredient.energie_kJ)

            if isinstance(ingredient.ingredient.energie_kcal, float):
                total_calorique_kcal  = total_calorique_kcal + ingredient.quantity * (ingredient.ingredient.energie_kcal)
            
            if isinstance(ingredient.ingredient.glucide , float):
                total_glucide  = total_glucide + ingredient.quantity * (ingredient.ingredient.glucide)

            if isinstance(ingredient.ingredient.sodium , float):
                total_sodium  = total_sodium + ingredient.quantity * (ingredient.ingredient.sodium)

            if isinstance(ingredient.ingredient.sodium , float):
                total_sel  = total_sel + ingredient.quantity * (ingredient.ingredient.selchlorure)


            if isinstance(ingredient.ingredient.energie_kJ, float):
                total_proteins  = total_proteins + ingredient.quantity * (ingredient.ingredient.proteins)

            if isinstance(ingredient.ingredient.fibres, float):
                total_fibres  = total_fibres + ingredient.quantity * (ingredient.ingredient.fibres)
            
            if isinstance(ingredient.ingredient.eau , float):
                total_eau  = total_eau + ingredient.quantity * (ingredient.ingredient.eau)

            if isinstance(ingredient.ingredient.lipide , float):
                total_lipide  = total_lipide + ingredient.quantity * (ingredient.ingredient.lipide)



            if isinstance(ingredient.ingredient.sucres, float):
                total_sucres  = total_sucres + ingredient.quantity * (ingredient.ingredient.sucres)

            if isinstance(ingredient.ingredient.fructose, float):
                total_fructose  = total_fructose + ingredient.quantity * (ingredient.ingredient.fructose)
            
            if isinstance(ingredient.ingredient.galactose , float):
                total_galactose  = total_galactose + ingredient.quantity * (ingredient.ingredient.galactose)

            if isinstance(ingredient.ingredient.glucose , float):
                total_glucose  = total_glucose + ingredient.quantity * (ingredient.ingredient.glucose)

            if isinstance(ingredient.ingredient.lactose, float):
                total_lactose  = total_lactose + ingredient.quantity * (ingredient.ingredient.lactose)

            if isinstance(ingredient.ingredient.maltose, float):
                total_maltose  = total_maltose + ingredient.quantity * (ingredient.ingredient.maltose)

            if isinstance(ingredient.ingredient.saccharose, float):
                total_saccharose  = total_saccharose + ingredient.quantity * (ingredient.ingredient.saccharose)
            
            if isinstance(ingredient.ingredient.amidon , float):
                total_amidon  = total_amidon + ingredient.quantity * (ingredient.ingredient.amidon)

            if isinstance(ingredient.ingredient.fibresALimentraires , float):
                total_fibresAlimentaires  = total_fibresAlimentaires + ingredient.quantity * (ingredient.ingredient.fibresALimentraires)

            if isinstance(ingredient.ingredient.polyols, float):
                total_polyols  = total_polyols + ingredient.quantity * (ingredient.ingredient.polyols)


            if isinstance(ingredient.ingredient.cendres , float):
                total_cendres  = total_cendres + ingredient.quantity * (ingredient.ingredient.cendres)

            if isinstance(ingredient.ingredient.alcool , float):
                total_alcool  = total_alcool + ingredient.quantity * (ingredient.ingredient.alcool)

            if isinstance(ingredient.ingredient.acidesOrganiques, float):
                total_acidesOrganiques  = total_acidesOrganiques + ingredient.quantity * (ingredient.ingredient.acidesOrganiques)


            if isinstance(ingredient.ingredient.AGsatures, float):
                total_AGsatures  = total_AGsatures + ingredient.quantity * (ingredient.ingredient.AGsatures)

            if isinstance(ingredient.ingredient.AGmonoinsature, float):
                total_AGmonoinsature  = total_AGmonoinsature + ingredient.quantity * (ingredient.ingredient.AGmonoinsature)

            if isinstance(ingredient.ingredient.AGpolyinsature, float):
                total_AGpolyinsature  = total_AGpolyinsature + ingredient.quantity * (ingredient.ingredient.AGpolyinsature)
            
            if isinstance(ingredient.ingredient.AGbutyrique , float):
                total_AGbutyrique  = total_AGbutyrique + ingredient.quantity * (ingredient.ingredient.AGbutyrique)

            if isinstance(ingredient.ingredient.AGcaproique , float):
                total_AGcaproique  = total_AGcaproique + ingredient.quantity * (ingredient.ingredient.AGcaproique)

            if isinstance(ingredient.ingredient.AGcaprylique, float):
                total_AGcaprylique  = total_AGcaprylique + ingredient.quantity * (ingredient.ingredient.AGcaprylique)

            if isinstance(ingredient.ingredient.AGcaprique , float):
                total_AGcaprique  = total_AGcaprique + ingredient.quantity * (ingredient.ingredient.AGcaprique)

            if isinstance(ingredient.ingredient.AGlaurique , float):
                total_AGlaurique  = total_AGlaurique + ingredient.quantity * (ingredient.ingredient.AGlaurique)

            if isinstance(ingredient.ingredient.AGmyristique, float):
                total_AGmyristique  = total_AGmyristique + ingredient.quantity * (ingredient.ingredient.AGmyristique)

            if isinstance(ingredient.ingredient.AGpalmitique , float):
                total_AGpalmitique  = total_AGpalmitique + ingredient.quantity * (ingredient.ingredient.AGpalmitique)

            if isinstance(ingredient.ingredient.AGbstearique, float):
                total_AGbstearique  = total_AGbstearique + ingredient.quantity * (ingredient.ingredient.AGbstearique)

            if isinstance(ingredient.ingredient.AGoleique , float):
                total_AGoleique  = total_AGoleique + ingredient.quantity * (ingredient.ingredient.AGoleique)

            if isinstance(ingredient.ingredient.AGlinoleique , float):
                total_AGlinoleique  = total_AGlinoleique + ingredient.quantity * (ingredient.ingredient.AGlinoleique)

            if isinstance(ingredient.ingredient.AGalphalinolenique , float):
                total_AGalphalinolenique  = total_AGalphalinolenique + ingredient.quantity * (ingredient.ingredient.sodium)

            if isinstance(ingredient.ingredient.AGepa, float):
                total_AGepa  = total_AGepa + ingredient.quantity * (ingredient.ingredient.AGepa)

            if isinstance(ingredient.ingredient.AGdha, float):
                total_AGdha  = total_AGdha + ingredient.quantity * (ingredient.ingredient.AGdha)

            if isinstance(ingredient.ingredient.cholesterol, float):
                total_cholesterol  = total_cholesterol + ingredient.quantity * (ingredient.ingredient.cholesterol)

            if isinstance(ingredient.ingredient.selchlorure , float):
                total_selchlorure  = total_selchlorure + ingredient.quantity * (ingredient.ingredient.selchlorure)

            if isinstance(ingredient.ingredient.calcium, float):
                total_calcium  = total_calcium + ingredient.quantity * (ingredient.ingredient.calcium)

            if isinstance(ingredient.ingredient.cuivre, float):
                total_cuivre  = total_cuivre + ingredient.quantity * (ingredient.ingredient.cuivre)

            if isinstance(ingredient.ingredient.fer , float):
                total_fer  = total_fer + ingredient.quantity * (ingredient.ingredient.fer)

            if isinstance(ingredient.ingredient.iode , float):
                total_iode  = total_iode + ingredient.quantity * (ingredient.ingredient.iode)

            if isinstance(ingredient.ingredient.magnesium, float):
                total_magnesium  = total_magnesium + ingredient.quantity * (ingredient.ingredient.magnesium)



            if isinstance(ingredient.ingredient.manganese, float):
                total_manganese  = total_manganese + ingredient.quantity * (ingredient.ingredient.manganese)

            if isinstance(ingredient.ingredient.phosphore , float):
                total_phosphore  = total_phosphore + ingredient.quantity * (ingredient.ingredient.phosphore)

            if isinstance(ingredient.ingredient.potassium, float):
                total_potassium  = total_potassium + ingredient.quantity * (ingredient.ingredient.potassium)

            if isinstance(ingredient.ingredient.selenium , float):
                total_selenium  = total_selenium + ingredient.quantity * (ingredient.ingredient.selenium)

            if isinstance(ingredient.ingredient.zinc , float):
                total_zinc  = total_zinc + ingredient.quantity * (ingredient.ingredient.zinc)

            if isinstance(ingredient.ingredient.retinol, float):
                total_retinol  = total_retinol + ingredient.quantity * (ingredient.ingredient.retinol)

            if isinstance(ingredient.ingredient.betaCarotene , float):
                total_betacarotene  = total_betacarotene + ingredient.quantity * (ingredient.ingredient.betaCarotene)

            if isinstance(ingredient.ingredient.vitamineD , float):
                total_vitamineD  = total_vitamineD + ingredient.quantity * (ingredient.ingredient.vitamineD)

            if isinstance(ingredient.ingredient.vitamineE, float):
                total_vitamineE  = total_vitamineE + ingredient.quantity * (ingredient.ingredient.vitamineE)
            if isinstance(ingredient.ingredient.VitamineK1 , float):
                total_VitamineK1  = total_VitamineK1 + ingredient.quantity * (ingredient.ingredient.VitamineK1)

            if isinstance(ingredient.ingredient.vitamineK2 , float):
                total_vitamineK2  = total_vitamineK2 + ingredient.quantity * (ingredient.ingredient.vitamineK2)

            if isinstance(ingredient.ingredient.vitamineB1, float):
                total_vitamineB1  = total_vitamineB1 + ingredient.quantity * (ingredient.ingredient.vitamineB1)

            
            if isinstance(ingredient.ingredient.vitamineB2, float):
                total_vitamineB2  = total_vitamineB2 + ingredient.quantity * (ingredient.ingredient.vitamineB2)

#####vitamineB2

            if isinstance(ingredient.ingredient.VitamineB3 , float):
                total_vitamineB3  = total_vitamineB3 + ingredient.quantity * (ingredient.ingredient.VitamineB3)

            if isinstance(ingredient.ingredient.vitamineB5 , float):
                total_VitamineB5  = total_VitamineB5 + ingredient.quantity * (ingredient.ingredient.vitamineB5)

            if isinstance(ingredient.ingredient.vitamineB9, float):
                total_vitamineB6  = total_vitamineB6 + ingredient.quantity * (ingredient.ingredient.vitamineB6)
            if isinstance(ingredient.ingredient.glucide , float):
                total_VitamineB9  = total_VitamineB9 + ingredient.quantity * (ingredient.ingredient.vitamineB9)
#Changing V to V
            if isinstance(ingredient.ingredient.VitamineB12 , float):
                total_vitamineB12  = total_vitamineB12 + ingredient.quantity * (ingredient.ingredient.VitamineB12)

                
            if isinstance(ingredient.quantity, float):
                quantite_total  = quantite_total + ingredient.quantity 

        quantite_total = quantite_total - Total_eau_ajoutee


        total_AG_trans = total_AGsatures +  total_AGbutyrique + total_AGcaproique + total_AGcaprylique + total_AGcaprique + total_AGlaurique
        + total_AGmyristique + total_AGpalmitique + total_AGbstearique + total_AGoleique + total_AGlinoleique + total_AGalphalinolenique
        + total_AGepa + total_AGdha

        total_AG_insatures = total_AGmonoinsature + total_AGpolyinsature

        total_AG = total_AG_trans + total_AG_insatures + total_AGsatures
        total_VitamineK = total_VitamineK1 + total_vitamineK2

        return {"total_calorique" : total_calorique / quantite_total, "total_calorique_kcal" : total_calorique_kcal/quantite_total,
                "total_glucide" : total_glucide / quantite_total, "total_sodium" : total_sodium / quantite_total, 
                "total_sel" : total_sel/quantite_total, 
                "total_proteins" : total_proteins / quantite_total, "total_fibres" : total_fibres / quantite_total, 
                "total_eau" : total_eau / quantite_total, "total_sodium" : total_sodium / quantite_total, 
                "total_lipide" : total_lipide / quantite_total, "total_sucres" : total_sucres / quantite_total, 
                "total_fructose" : total_fructose / quantite_total, "total_galactose" : total_galactose / quantite_total, 
                "total_glucose" : total_glucose / quantite_total, "total_lactose" : total_lactose / quantite_total, 
                "total_maltose" : total_maltose / quantite_total, "total_saccharose" : total_saccharose / quantite_total, 
                "total_amidon" : total_amidon / quantite_total, "total_fibresAlimentaires" : total_fibresAlimentaires / quantite_total, 
                "total_polyols" : total_polyols / quantite_total, "total_cendres" : total_cendres / quantite_total, 
                "total_alcool" : total_alcool / quantite_total, "total_acidesOrganiques" : total_acidesOrganiques / quantite_total, 
                "total_AGsatures" : total_AGsatures / quantite_total, "total_AGmonoinsature" : total_AGmonoinsature / quantite_total, 
                "total_AGpolyinsature" : total_AGpolyinsature / quantite_total, "total_AGbutyrique" : total_AGbutyrique / quantite_total, 
                "total_AGcaproique" : total_AGcaproique / quantite_total, "total_AGcaprylique" : total_AGcaprylique / quantite_total, 
                "total_AGcaprique" : total_AGcaprique / quantite_total, "total_AGlaurique" : total_AGlaurique / quantite_total, 
        
                "total_AGmyristique" : total_AGmyristique / quantite_total, "total_AGpalmitique" : total_AGpalmitique / quantite_total, 

                "total_AGbstearique" : total_AGbstearique / quantite_total, "total_AGoleique" : total_AGoleique / quantite_total, 

                "total_AGlinoleique" : total_AGlinoleique / quantite_total, "total_AGalphalinolenique" : total_AGalphalinolenique / quantite_total, 

                        
                "total_AGepa" : total_AGepa / quantite_total, "total_AGdha" : total_AGdha / quantite_total, "total_cholesterol" : total_cholesterol / quantite_total, 

                "total_selchlorure" : total_selchlorure / quantite_total, "total_cuivre" : total_cuivre / quantite_total, 

                "total_fer" : total_fer / quantite_total, "total_iode" : total_iode / quantite_total, 

                "total_magnesium" : total_magnesium / quantite_total, "total_manganese" : total_manganese / quantite_total, "total_calcium" : total_calcium / quantite_total, 

                "total_phosphore" : total_phosphore / quantite_total, "total_potassium" : total_potassium / quantite_total, 

                "total_selenium" : total_selenium / quantite_total, "total_zinc" : total_zinc / quantite_total, 
                
                "total_retinol" : total_retinol / quantite_total, "total_betacarotene" : total_betacarotene / quantite_total, 

                "total_vitamineD" : total_vitamineD / quantite_total, "total_vitamineE" : total_vitamineE / quantite_total, 

                "total_VitamineK1" : total_VitamineK1 / quantite_total, "total_vitamineK2" : total_vitamineK2 / quantite_total, 


                "total_vitamineK" : total_VitamineK1 + total_vitamineK2/ quantite_total, 

                    
                "total_vitamineB1" : total_vitamineB1 / quantite_total, "total_vitamineB2" : total_vitamineB2 / quantite_total, 

                "total_vitamineB3" : total_vitamineB3 / quantite_total, "total_VitamineB5" : total_VitamineB5 / quantite_total, 

                "total_vitamineB6" : total_vitamineB6 / quantite_total, "total_VitamineB9" : total_VitamineB9 / quantite_total,  

                "total_VitamineB12" : total_vitamineB12 / quantite_total,   "total_sels_ajoutes" : total_sels_ajoutes / quantite_total , 
                 
                "total_sucres_ajoutes" : 100*total_sucres_ajoutes / quantite_total, "total_graisses_ajoutes" : 100 * Total_graisses_ajoutes / quantite_total, "total_fruitslegumineuse" : 100 * Total_fruitslegumineuse / quantite_total ,
                "total_AG" : total_AGsatures + total_AGmonoinsature + total_AGpolyinsature , "total_AG_insatures" : total_AGmonoinsature + total_AGpolyinsature, "total_AG_trans" : 0, "Quantite_totale" : quantite_total,
                "total_eau_ajoutee" : Total_eau_ajoutee,}


    def score_calorie_kj( total_calorique) : 
        '''Calculer un score selon le total obtenu'''
        arrondi = round( total_calorique,1 )
        if arrondi <= 335 : 
            return 0
        elif arrondi <= 670:
            return 1 
        elif arrondi <= 1005 : 
            return 2
        elif arrondi <= 1340 :
            return 3 
        elif arrondi <= 1675 : 
            return 4
        elif arrondi <= 2010 :
            return 5 
        elif arrondi <= 2345 : 
            return 6
        elif arrondi <= 2680 :
            return 7 
        elif arrondi <= 3015 : 
            return 8
        elif arrondi <= 3350 :
            return 9
        else :
            return 10


    def score_sodium( total_sodium) : 

        arrondi = round( total_sodium,2 )
        if arrondi <= 90 : 
            return 0
        elif arrondi <= 180:
            return 1 
        elif arrondi <= 270 : 
            return 2
        elif arrondi <= 360 :
            return 3 
        elif arrondi <= 450 : 
            return 4
        elif arrondi <= 540 :
            return 5 
        elif arrondi <= 630 : 
            return 6
        elif arrondi <= 720 :
            return 7 
        elif arrondi <= 810 : 
            return 8
        elif arrondi <= 900 :
            return 9
        else :
            return 10 

    def score_glucide(total_glucide) : 
        ''' Calculer score de glucide '''

        arrondi = round( total_glucide,2)
        if arrondi <= 4.5 : 
            return 0
        elif arrondi <= 9:
            return 1 
        elif arrondi <= 13.5 : 
            return 2
        elif arrondi <= 18 :
            return 3 
        elif arrondi <= 22.5 : 
            return 4
        elif arrondi <= 27 :
            return 5 
        elif arrondi <= 31 : 
            return 6
        elif arrondi <= 36 :
            return 7 
        elif arrondi <= 40 : 
            return 8
        elif arrondi <= 45 :
            return 9
        else :
            return 10

    def score_agsature( total_agsature) : 
        ''' Calculer score d'acides gras saturés '''

        arrondi = round( total_agsature,1)
        if arrondi <= 1 : 
            return 0
        elif arrondi <= 2:
            return 1 
        elif arrondi <= 3 : 
            return 2
        elif arrondi <= 4 :
            return 3 
        elif arrondi <= 5 : 
            return 4
        elif arrondi <= 6 :
            return 5 
        elif arrondi <= 7 : 
            return 6
        elif arrondi <= 8 :
            return 7 
        elif arrondi <= 9 : 
            return 8
        elif arrondi <= 10 :
            return 9
        else :
            return 10

    def score_protein(total_protein) : 
        ''' Calculer score de protein '''

        arrondi = round( total_protein,2)
        if arrondi <= 1.6 : 
            return 0
        elif arrondi <= 3.2:
            return 1 
        elif arrondi <= 4.8 : 
            return 2
        elif arrondi <= 6.4 :
            return 3 
        elif arrondi <= 8 : 
            return 4
        else :
            return 5

    def score_fibre(total_fibre) : 
        ''' Calculer score de fibres '''
        arrondi = round( total_fibre,2)
        if arrondi <= 0.9 : 
            return 0
        elif arrondi <= 1.9:
            return 1 
        elif arrondi <= 2.8 : 
            return 2
        elif arrondi <= 3.7 :
            return 3 
        elif arrondi <= 4.7 : 
            return 4
        else :
            return 5


    def score_fln(total_graisse, total_fruitslegumes) : 
        ''' Calculer score de fruit légumes et légumineuse '''
        arrondi = round( total_graisse + total_fruitslegumes ,1)
        if arrondi <= 40 : 
            return 0
        elif arrondi <= 60:
            return 1 
        elif arrondi <= 80 : 
            return 2
        else :
            return 5

    def score_A(pts_kj, pts_glucide, pts_agsatures, pts_sodium) : 
        ''' Calculer score A '''
        score =  pts_kj + pts_glucide + pts_agsatures + pts_sodium
        return score

    def nutriscore(scoreA, pts_fln, pts_prot, pts_fib):
        ''' Attribuer un nutriscore selon les scores calculés'''
        if (scoreA < 11 and scoreA > 0) or (scoreA >= 11 and pts_fln == 5) : 
            return scoreA - (pts_prot + pts_fln)

        else :
            return scoreA - pts_fln - pts_fib

    def nutriscoreLettre(nutriscore):
        if nutriscore < 0 : 
            return "Nutriscore A"
        elif nutriscore < 3 :
            return "Nutriscore B"
        elif nutriscore < 11 :
            return "Nutriscore C"  
        elif nutriscore < 19 :
            return "Nutriscore D"
        else :
            return "Nutriscore E"


    def allegation(total_cal, total_graisse, total_ag_saturee,
     total_ag_trans, total_ag, total_sucres, total_sucres_ajoutes, total_sel, total_sodium, total_sel_ajoute, 
     total_fibre, total_protein, total_graisses_monoinsatures, total_graisses_polyinsatures,
     total_selenium,  total_magnesium, total_phosphore, total_calcium, total_cuivre, total_fer, 
     total_manganese, total_potassium, total_zinc, total_vitamineD, total_vitamineE,
     total_vitamineK, total_vitamineB1,  total_vitamineB2, total_vitamineB3, total_vitamineB5, 
     total_vitamineB6, total_vitamineB9, total_vitamineB12, total_AGepa, total_dha, total_AGalphalinolenique  ) : 
        '''faire une allégation selon les valeurs des différents totaux'''
        allegations = []
        allegations_valeurs = []

        allegations_minerales = []
        allegations_minerales_valeurs = []


        allegations_vitamine_valeurs = []
        allegations_vitamine = []


        if total_cal < 170 : 
            allegations.append('Faible en valeur énergétique' )
            allegations_valeurs.append(round(total_cal, 5))
        elif total_cal < 17 : 
            allegations_valeurs.append(round(total_cal, 5))
            allegations.append('Sans apport energetique')

        #ajouter acide gras trans  
        if total_graisse < 3 :
            allegations.append ('faible teneur en matières grasses')
            allegations_valeurs.append(round(total_graisse, 5))
        
        elif total_graisse < 0.5 :
            allegations.append ('sans matières grasses' )
            allegations_valeurs.append(total_graisse)
        
        #à voir avec le client    
        if total_ag_saturee + total_ag_trans < 1.5 :
            allegations.append ('faible teneur en graisses saturees')
            allegations_valeurs.append(round(total_ag_saturee + total_ag_trans, 5))

        elif total_ag_saturee + total_ag_trans < 0.1 :
            allegations.append ('faible teneur en graisses saturees')    
            allegations_valeurs.append(round(total_ag_saturee + total_ag_trans, 5))
        
        if total_sucres_ajoutes < 5 :
            allegations.append ('faible teneur en sucres')
            allegations_valeurs.append(round(total_sucres_ajoutes, 5))

        elif total_sucres_ajoutes < 0.5 :
            allegations.append ('sans sucres')
            allegations_valeurs.append(round(total_sucres_ajoutes, 5))
        
        if total_sucres_ajoutes < 2 :
            allegations.append ('Sans sucre ajouté')
            allegations_valeurs.append(round(total_sucres_ajoutes, 5))

        #à voir avec le client 
        #if total_sucres_ajoutes < 0.5 :
        #    allegations.append ({'sans sucres ajoutes' : total_sucres})    
        
        if total_sel + total_sodium < 0.12 :
            allegations.append ('pauvre en sel')
            allegations_valeurs.append(round(total_sel + total_sodium, 5))   

        elif total_sel + total_sodium < 0.04 :
            allegations.append ('tres pauvre en sel') 
            allegations_valeurs.append(round(total_sel + total_sodium, 5))   
        
        elif total_sel + total_sodium < 0.005 :
            allegations.append ('sans sodium')  
            allegations_valeurs.append(round(total_sel + total_sodium,5)) 

        if total_sel_ajoute < 0.005 :
            allegations.append ('sans sodium ou sel ajouté') 
            allegations_valeurs.append(round(total_sel_ajoute, 5))  

        #a voir avec le client
        if total_fibre > 3 :
            allegations.append ('source de fibres')  
            allegations_valeurs.append(round(total_fibre, 5))   

        elif total_fibre > 6 :
            allegations.append ('riche en fibres')
            allegations_valeurs.append(round(total_fibre, 5)) 

        #a voir avec le client
        if total_cal > 0 : 
            if total_protein * 4 / total_cal > 0.12 :
                allegations.append ('source de proteins')
                allegations_valeurs.append(round(total_protein * 4 / total_cal, 5)) 

            elif total_protein * 4 / total_cal > 0.20 :
                allegations.append ('riche en proteins')
                allegations_valeurs.append(round(total_protein * 4 / total_cal, 5)) 
    


        ### 22, 23, 24 
        if (total_AGepa + total_dha > 40) : 
            allegations.append ('source d acide gras omega3')
            allegations_valeurs.append (round(total_AGepa + total_dha ,5) )

        elif total_AGalphalinolenique > 0.3 : 
            allegations.append ('source d acide gras omega3')
            allegations_valeurs.append (round(total_AGepa + total_dha,5))

        elif (total_AGepa + total_dha > 80) : 
            allegations.append ('riche en acide gras omega3')
            allegations_valeurs.append (round(total_AGepa + total_dha,5))

        elif total_AGalphalinolenique > 0.6 : 
            allegations.append ('riche en acide gras omega3')
            allegations_valeurs.append(round(total_AGalphalinolenique, 5))

        total_acide_gras = total_graisses_monoinsatures + total_graisses_polyinsatures + total_ag_saturee

        if total_acide_gras > 0 :
            if total_graisse == 0:
                total_graisse = 1

            if (total_graisses_monoinsatures / total_graisse > 0.45 and total_graisses_monoinsatures * 9 > 0.2 * total_cal) : 
                allegations.append ('riche en graisse monoinsaturees')
                allegations_valeurs.append(round(total_graisses_monoinsatures / total_graisse, 5))

            if (total_graisses_polyinsatures / total_graisse  > 0.45 and total_graisses_polyinsatures * 9> 0.2 * total_cal) : 
                allegations.append ('riche en graisse polyinsaturees')
                allegations_valeurs.append(round(total_graisses_monoinsatures / total_graisse, 5))

            if ( total_graisses_polyinsatures + total_graisses_monoinsatures / total_graisse > 0.7  and total_graisses_polyinsatures + total_graisses_monoinsatures * 9 > 0.2 * total_cal) : 
                allegations.append ('riche en graisse insaturees')
                allegations_valeurs.append(round(total_graisses_monoinsatures / total_graisse, 5))

#########################################################################################33
#
#       Minéraux
#
######################################################################################
        if total_selenium > 8.25 : 
            allegations_minerales.append('source de selenium')
            allegations_minerales_valeurs.append(round(total_selenium,5))
        elif total_selenium > 16.5 : 
            allegations_minerales.append('riche en selenium')
            allegations_minerales_valeurs.append(round(total_selenium,5))         

        if total_magnesium > 0.056 : 
            allegations_minerales.append('source de magnesium')
            allegations_minerales_valeurs.append(round(total_magnesium,5))
        elif total_magnesium > 0.112 : 
            allegations_minerales.append('riche en magnesium')
            allegations_minerales_valeurs.append(round(total_magnesium,5))

        if total_phosphore > 0.105 : 
            allegations_minerales.append('source de phosphore')
            allegations_minerales_valeurs.append(round(total_phosphore,5))

        elif total_phosphore > 0.210 : 
            allegations_minerales.append('riche en phosphore')
            allegations_minerales_valeurs.append(round(total_phosphore,5))

        if total_calcium > 120 : 
            allegations_minerales.append('source de calcium')
            allegations_minerales_valeurs.append(round(total_calcium, 5))
        elif total_calcium > 240 : 
            allegations_minerales.append('riche en selenium')
            allegations_minerales_valeurs.append(round(total_calcium, 5))

        if total_cuivre > 0.15 : 
            allegations_minerales.append('source de cuivre')
            allegations_minerales_valeurs.append(round(total_cuivre, 5))
        elif total_cuivre > 0.30 : 
            allegations_minerales.append('riche en cuivre')
            allegations_minerales_valeurs.append(round(total_cuivre, 5))

        if total_fer > 2.1 : 
            allegations_minerales.append('source de fer')
            allegations_minerales_valeurs.append(round(total_fer, 5))
        elif total_fer > 4.2 : 
            allegations_minerales.append('riche en fer')
            allegations_minerales_valeurs.append(round(total_fer, 5))

        if total_manganese > 0.3 : 
            allegations_minerales.append('source de manganese')
            allegations_minerales_valeurs.append(round(total_manganese,5))
        elif total_manganese > 0.6 : 
            allegations_minerales.append('riche en manganese')
            allegations_minerales_valeurs.append(round(total_manganese, 5))

        if total_potassium > 300 : 
            allegations_minerales.append('source de potassium')
            allegations_minerales_valeurs.append(round(total_potassium, 5))
        elif total_potassium > 600 : 
            allegations_minerales.append('riche en potassium')    
            allegations_minerales_valeurs.append(round(total_potassium, 5))

        if total_zinc > 1.5 : 
            allegations_minerales.append('source de zinc')
            allegations_minerales_valeurs.append(round(total_zinc, 5))
        elif total_zinc > 3 : 
            allegations_minerales.append('riche en zinc')
            allegations_minerales_valeurs.append(round(total_zinc, 5))

#############################################################
#
#
#####################################################################

        if total_vitamineD > 0.75 : 
            allegations_vitamine.append('source de vitamine D')
            allegations_vitamine_valeurs.append(round(total_vitamineD, 5))
        elif total_vitamineD > 1.5 : 
            allegations_vitamine.append('riche en vitamine D')
            allegations_vitamine_valeurs.append(round(total_vitamineD, 5))

        if total_vitamineE > 1.8 : 
            allegations_vitamine.append('source de vitamine E')
            allegations_vitamine_valeurs.append(round(total_vitamineE,5))
        elif total_vitamineE > 1.8 : 
            allegations_vitamine.append('riche en vitamine E')
            allegations_vitamine_valeurs.append(round(total_vitamineE, 5))
            
        if total_vitamineK > 1.8 : 
            allegations_vitamine.append('source de vitamine K')
            allegations_vitamine_valeurs.append(round(total_vitamineK,5))
        elif total_vitamineK > 1.8 : 
            allegations_vitamine.append('riche en vitamine K')
            allegations_vitamine_valeurs.append(round(total_vitamineK,5))            
            
        if total_vitamineB1 > 0.165 : 
            allegations_vitamine.append('source de vitamine B1')
            allegations_vitamine_valeurs.append(round(total_vitamineB1,5))
        elif total_vitamineB1 > 0.33 : 
            allegations_vitamine.append('riche en vitamine B1')     
            allegations_vitamine_valeurs.append(round(total_vitamineB1,5))

        if total_vitamineB2 > 0.21 : 
            allegations_vitamine.append('source de vitamine B2')
            allegations_vitamine_valeurs.append(round(total_vitamineB2, 5))
        elif total_vitamineB2 > 0.42 : 
            allegations_vitamine.append('riche en vitamine B2') 
            allegations_vitamine_valeurs.append(round(total_vitamineB2, 5))    


        if total_vitamineB3 > 2.4 : 
            allegations_vitamine.append('source de vitamine B2')
            allegations_vitamine_valeurs.append(round(total_vitamineB3,5))
        elif total_vitamineB3 > 4.2 : 
            allegations_vitamine.append('riche en vitamine B2') 
            allegations_vitamine_valeurs.append(round(total_vitamineB3,5))   

        if total_vitamineB5 > 0.9 : 
            allegations_vitamine.append('source de vitamine B5')
            allegations_vitamine_valeurs.append(round(total_vitamineB5,5))
        elif total_vitamineB5 > 1.8 : 
            allegations_vitamine.append('riche en vitamine B5')  
            allegations_vitamine_valeurs.append(round(total_vitamineB5,5))   

        if total_vitamineB6 > 0.21 : 
            allegations_vitamine.append('source de vitamine B6')
            allegations_vitamine_valeurs.append(round(total_vitamineB6,5))
        elif total_vitamineB6 > 0.42 : 
            allegations_vitamine.append('riche en vitamine B6')
            allegations_vitamine_valeurs.append(round(total_vitamineB6,5))

        if total_vitamineB9 > 30 : 
            allegations_vitamine.append('source de vitamine B9')
            allegations_vitamine_valeurs.append(round(total_vitamineB9,5))
        elif total_vitamineB9 > 60 : 
            allegations_vitamine.append('riche en vitamine B9')
            allegations_vitamine_valeurs.append(round(total_vitamineB9,5))

        if total_vitamineB12 > 0.375 : 
            allegations_vitamine.append('source de vitamine B12')
            allegations_vitamine_valeurs.append(round(total_vitamineB12,5))
        elif total_vitamineB12 > 0.75: 
            allegations_vitamine.append('riche en vitamine B12')
            allegations_vitamine_valeurs.append(round(total_vitamineB12,5))

        return allegations, allegations_minerales, allegations_vitamine, allegations_valeurs, allegations_minerales_valeurs, allegations_vitamine_valeurs


#############################################################################################################################
#
# Declare necessary data 
#
#######################################################################################################
    nutriscore_couleur = {"Nutriscore A" : "Vert", "Nutriscore B" : "Vert_clair", "Nutriscore C" : "Jaune", "Nutriscore D" : "Orange Clair", "Nutriscore E" : "Orange Foncé", }
    ingredient_Recipe = models.IngredientRecipe.objects.filter(recipe = recipe)
    ingredients = models.IngredientRecipe.objects.filter(recipe = recipe)



    total_calorique = 0 
    for ingredient in ingredients : 
        if isinstance(ingredient.ingredient.energie_kJ, float):
            total_calorique  = total_calorique + ingredient.quantity * (ingredient.ingredient.energie_kJ/100)

    context = {'object' : recipe, 'ingredients' : ingredients}
    context['recipe'] = recipe

    #context['total_calorie'] = total_calorie()
    #context['Score_calorie'] = score_calorie_kj()

    process_Recipe = models.ProcessRecipe.objects.filter(recipe = recipe)
    cooking_Recipe = models.CookingRecipe.objects.filter(recipe = recipe)
    poids_unitaire = 12.5
    poids_cru_unitaire = 12.5

    if len(models.WeigthRecipe.objects.filter(recipe = recipe)) > 0 :
        weight_Recipe = models.WeigthRecipe.objects.filter(recipe = recipe)[0]

        poids_unitaire = weight_Recipe.unitaire
        poids_cru_unitaire = weight_Recipe.cru
        context['poids_unitaire'] = poids_unitaire
        context['poids_cru'] = poids_cru_unitaire
        
    else :
        context['poids_unitaire'] = poids_unitaire
        context['poids_cru'] = poids_cru_unitaire



    '''for i in range(len(ingredient_Recipe)) : 
        if ingredient_Recipe[i].recipe.famille == models.Famille.objects.get(name = 'viandes, œufs, poissons et assimilés'):
            score_fln = score_fln + ingredient_Recipe[i].quantity
    '''

    context['ingredients'] = ingredient_Recipe
    context['process'] = process_Recipe
    context['cooking'] = cooking_Recipe

    totaux = total_calorie()

    
# Pourcentage après cuisson        
    q_total = totaux["Quantite_totale"]
    perc = []
    if q_total > 0 :
        for i in range (len(ingredient_Recipe)) :
            perc.append( round(ingredient_Recipe[i].quantity / q_total * 100,2)) 
    
    else :
        perc = [0 for i in len(ingredient_Recipe)]        
    context['perc_ingredients'] = perc


    # Pourcentage avant cuisson        
    q_total_eau = totaux["Quantite_totale"] + totaux['total_eau_ajoutee']
    perc_eau = []
    if q_total_eau > 0 :
        for i in range (len(ingredient_Recipe)) :
            perc_eau.append( round(ingredient_Recipe[i].quantity / q_total_eau * 100,2)) 
    
    else :
        perc_eau = [0 for i in len(ingredient_Recipe)]        
    context['perc_ingredients_eau'] = perc_eau



###########################################################################################
#
#   Envoi des quantites calculees au front end
#
############################################################################################

    
    context['quantite_totale'] = totaux["Quantite_totale"]
    context['inv_quantite_totale'] = 1/totaux["Quantite_totale"]



    context['total_glucide'] = round(totaux["total_glucide"],2)
    context['total_sodium'] = round(totaux["total_sodium"], 5)

    context['total_protein'] = round(totaux['total_proteins'],5)
    context['total_fibre'] = round(totaux["total_fibres"],5)
    context['total_eau'] = round(totaux["total_eau"],2)
    context['total_lipide'] = round(totaux["total_lipide"],2)

    context['total_sucres'] = round(totaux['total_sucres'],5)
    context['total_fructose'] = round(totaux["total_fructose"],5)
    context['total_galactose'] = round(totaux["total_galactose"],2)
    context['total_glucose'] = round(totaux["total_glucose"],2)
    context['total_lactose'] = round(totaux['total_lactose'],5)
    context['total_maltose'] = round(totaux["total_maltose"],5)
    context['total_saccharose'] = round(totaux["total_saccharose"],2)
    context['total_amidon'] = round(totaux["total_amidon"],2)
    context['total_fibresAlimentaires'] = round(totaux["total_fibresAlimentaires"],2)

    context['total_polyols'] = round(totaux['total_polyols'],5)
    context['total_cendres'] = round(totaux["total_cendres"],5)
    context['total_alcool'] = round(totaux["total_alcool"],2)
    context['total_acidesOrganiques'] = round(totaux["total_acidesOrganiques"],2)
    context['total_AGsatures'] = round(totaux['total_AGsatures'],5)
    context['total_AGmonoinsature'] = round(totaux["total_AGmonoinsature"],5)
    context['total_AGpolyinsature'] = round(totaux["total_AGpolyinsature"],2)
    context['total_AGbutyrique'] = round(totaux["total_AGbutyrique"],2)
    context['total_AGcaproique'] = round(totaux["total_AGcaproique"],2)
    context['total_AGcaprylique'] = round(totaux['total_AGcaprylique'],5)

    context['total_AGlaurique'] = round(totaux["total_AGlaurique"],5)
    context['total_AGmyristique'] = round(totaux["total_AGmyristique"],2)
    context['total_AGbutyrique'] = round(totaux["total_AGbutyrique"],2)
    context['total_AGpalmitique'] = round(totaux["total_AGpalmitique"],2)
    context['total_AGbstearique'] = round(totaux["total_AGbstearique"],2)
    context['total_AGoleique'] = round(totaux["total_AGoleique"],2)
    context['total_AGlinoleique'] = round(totaux["total_AGlinoleique"],2)
    context['total_AGalphalinolenique'] = round(totaux["total_AGalphalinolenique"],2)

    context['total_AGepa'] = round(totaux["total_AGepa"],5)
    context['total_AGdha'] = round(totaux["total_AGdha"],2)

    context['total_cholesterol'] = round(totaux["total_cholesterol"],2)
    context['total_selchlorure'] = round(totaux["total_selchlorure"],2)
    context['total_calcium'] = round(totaux["total_calcium"],2)
    context['total_cuivre'] = round(totaux["total_cuivre"],2)
    context['total_fer'] = round(totaux["total_fer"],2)
    context['total_iode'] = round(totaux['total_iode'],5)
    context['total_magnesium'] = round(totaux["total_magnesium"],2)
    context['total_manganese'] = round(totaux["total_manganese"],2)
    context['total_phosphore'] = round(totaux["total_phosphore"],2)
    context['total_potassium'] = round(totaux["total_potassium"],2)
    context['total_selenium'] = round(totaux["total_selenium"],2)
    context['total_zinc'] = round(totaux["total_zinc"],2)
    context['total_retinol'] = round(totaux["total_retinol"],2)
    context['total_betacarotene'] = round(totaux["total_betacarotene"],2)



    context['total_VitamineK1'] = round(totaux["total_VitamineK1"],2)
    context['total_vitamineK2'] = round(totaux["total_vitamineK2"],5)

    context['total_vitamineE'] = round(totaux["total_vitamineE"],5)
    context['total_vitamineB1'] = round(totaux['total_vitamineB1'],5)
    context['total_vitamineB2'] = round (totaux["total_vitamineB2"], 3)
    context['total_vitamineB3'] = round(totaux["total_vitamineB3"],5)

    context['total_VitamineB5'] = round(totaux['total_VitamineB5'],5)
    context['total_VitamineB9'] = round (totaux["total_VitamineB9"], 3)
    context['total_VitamineB12'] = round(totaux["total_VitamineB12"],5)


    context['total_sels_ajoutes'] = round(totaux['total_sels_ajoutes'],5)
    context['total_sucres_ajoutes'] = round (totaux["total_sucres_ajoutes"],10)
    context['Total_graisses_ajoutes'] = round(totaux['total_graisses_ajoutes'],5)
    context['Total_fruitslegumineuse'] = round (totaux["total_fruitslegumineuse"], 3)

    context['total_fln'] = round(totaux['total_graisses_ajoutes'] + totaux["total_fruitslegumineuse"],5)
    #get the total_fln quantite des ingredients appartenant a fruits, légumes ou légumineuses
    #context['total_fln'] = totaux['total_protein']


    #en kcal
    context['total_calorie_kcal'] = round(4* totaux["total_glucide"] + 4* totaux['total_proteins'] + 9* totaux["total_lipide"],5)

    #en kj 
    context['total_calorie'] = round(context['total_calorie_kcal']  * 4.18,5)


    context['Total_fln'] = round(totaux["total_graisses_ajoutes"] + totaux["total_fruitslegumineuse"],5)

#######################################################################################################################################
#
# Nutrition Fact per biscuit
#
######################################################################################################################################


    quantite_total = totaux['Quantite_totale']

    context['total_calorie_kcal_bis'] = round ((context['total_calorie_kcal'] / 100) * poids_unitaire, 2)
    context['total_calorie_bis'] = round( (context['total_calorie'] / 100) * poids_unitaire, 2) 

    context['total_calorie_kcal_gda'] = round (context['total_calorie_kcal_bis'] / 2000 *100, 2)
    context['total_calorie_gda'] = round ( context['total_calorie'] / 8400 * 100, 2)



    context['total_protein_nf'] = round (totaux['total_proteins'] , 2)
    context['total_protein_bis'] = round (totaux['total_proteins'] / 100 * poids_unitaire, 2)
    context['total_protein_gda'] = round (context['total_protein_bis'] / 50 * 100, 2)


    context['total_glucide_nf'] = round (totaux['total_glucide'],  2) 
    context['total_sucres_nf'] = round (totaux['total_sucres'], 2)
    context['total_glucide_bis'] = round (totaux['total_glucide'] / 100 * poids_unitaire, 2) 
    context['total_sucres_bis'] = round (totaux['total_sucres'] / 100 * poids_unitaire, 2)

    context['total_glucide_gda'] =  round (context['total_glucide_bis'] / 260 * 100, 2)
    context['total_sucres_gda'] =  round (context['total_sucres_bis'] / 90 * 100, 2)




    context['total_lipide_nf'] = round (totaux['total_lipide'], 2)
    context['total_AGsatures_nf'] = round(totaux['total_AGsatures'], 2)

    context['total_lipide_bis'] = round (totaux['total_lipide'] / 100 * poids_unitaire, 2)
    context['total_AGsatures_bis'] = round(totaux['total_AGsatures'] / 100 * poids_unitaire, 2)

    context['total_lipide_gda'] = round (context['total_lipide_bis'] / 70 * 100, 2)
    context['total_AGsatures_gda'] = round (context['total_AGsatures_bis'] / 20 * 100, 2)



    context['total_fibre_nf'] = round (totaux['total_fibres'] , 2)
    context['total_fibre_bis'] = round (totaux['total_fibres'] / 100 * poids_unitaire, 2)
    context['total_fibre_gda'] = round (context['total_fibre_bis'] / 25 * 100, 2)

    context['total_sels_ajoutes_nf'] = round (totaux['total_sels_ajoutes'], 2)
    context['total_sodium_bis'] = round (totaux["total_sels_ajoutes"] / 100 * poids_unitaire, 2)
    context['total_sodium_gda'] = round (context["total_sodium_bis"] / 2.4 * 100, 2)





#######################################################################################################################################
#
# Nutrition Fact GDA
#
######################################################################################################################################




    score_kj = score_calorie_kj(totaux["total_calorique"])
    score_sodium = score_sodium(totaux["total_sodium"])
    score_glucide = score_glucide(totaux['total_sucres'])
    score_agsatures = score_agsature(totaux["total_AGsatures"])
    score_protein = score_protein(totaux["total_proteins"])
    score_fibre = score_fibre(totaux["total_fibres"])
    score_fln = score_fln(totaux["total_graisses_ajoutes"], totaux["total_fruitslegumineuse"])

    scoreA = score_A(score_kj, score_glucide, score_agsatures, score_sodium)
    nutriscore = nutriscore(scoreA, score_fln, score_protein, score_fibre)  

    context['Score_sodium'] = score_sodium
    context['Score_kj'] = score_kj
    context['Score_glucide'] = score_glucide
    context['score_AGsatures'] = score_agsatures
    context['score_protein'] = score_protein
    context['score_fibre'] = score_fibre
    context['score_fln'] = score_fln
    context['score_A'] = scoreA
    #context['Score_calorie_kcal'] = 0        

    context['s'] = "rgba(95, 146, 48, 0.815)"

    context['nutriscore'] = nutriscoreLettre(nutriscore)
    context['couleur'] = nutriscore_couleur[context['nutriscore']]
    context['allegation'],context['allegation_minerales'],context['allegation_vitamine'], context['allegation_valeurs'], context['allegation_minerales_valeurs'], context['allegation_vitamine_valeurs'] = allegation(totaux["total_calorique"], totaux["total_graisses_ajoutes"], totaux["total_AGsatures"], totaux["total_AG_trans"],  totaux["total_AG"], totaux["total_sucres"],
                            totaux["total_sucres_ajoutes"], totaux["total_sel"], totaux["total_sodium"], totaux["total_sels_ajoutes"], totaux["total_fibres"], totaux["total_proteins"], totaux["total_AGmonoinsature"], totaux["total_AGpolyinsature"], 
                            totaux["total_selenium"], totaux["total_magnesium"], totaux["total_phosphore"], totaux["total_calcium"], totaux["total_cuivre"], totaux["total_fer"], totaux["total_manganese"], totaux["total_potassium"], totaux["total_zinc"], 
                            totaux["total_vitamineD"], totaux["total_vitamineE"], totaux["total_VitamineK1"] + totaux["total_vitamineK2"], totaux["total_vitamineB1"],  totaux["total_vitamineB2"], totaux["total_vitamineB3"], totaux["total_VitamineB5"], totaux["total_vitamineB6"], totaux["total_VitamineB9"],
                            totaux["total_VitamineB12"], totaux["total_AGepa"], totaux["total_AGdha"], totaux["total_AGalphalinolenique"] )
    #context.pop('self', None)
    #context['self'] = recipe_cont
    pdf = html_to_pdf("recipe/recipe_detail_pdf.html", context_dict = context)

    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')

@login_required
def home(request):
    context = {'title' : 'homme'}
    return render(request, "recipe/home.html", context)
    #return HttpResponse("<h1> Welcome to ORI </h1>")ß

'''def recettes(request):
    context = {'recipes' : recipes, 'title' : 'Recettes'}
    return render(request, "recipe/recettes.html", context)
    #return HttpResponse("<h1> Welcome to ORI </h1>")'''

def ingredients(request):
    context = {'ingredients' : ingredients_app, 'title' : 'Ingrédients'}
    return render(request, "recipe/ingredients.html", context)

def familles(request):
    context = {'familles' : familles_app, 'ingredients' : ingredients_app ,'title' : 'Ingrédients'}
    return render(request, "recipe/familles.html", context)

def contraintes(request):
    context = {'contraintes' : contraintes, 'title' : 'Ingrédients'}
    return render(request, "recipe/contraintes.html", context)





def create_recipe2(request) : 
    #form = form()
        #def form_valid(self, form):
        #form.instance.author = self.request.user
        #return super().form_valid(form)
    print(request)

    Formset_Params = {
    'ingredients_recipe-TOTAL_FORMS' : '1',
    'ingredients_recipe-INITIAL_FORMS' : '0',
    'ingredients_recipe-MIN_NUM_FORMS' : '1', 
    }    
    if request.method ==  "GET":
        form = RecipeForm()
        formset = IngredientFormSet(Formset_Params)
        #formset = IngredientFormSet()
        #return render(request, 'recipe/create_recipe.html', {"form" : form, "formset" : formset})
        return render(request, 'recipe/create_recipe.html', {"form" : form, "formset" : formset})

    elif request.method == "POST" :
        if 'terminerBttn' in request.POST:
            print(request.POST.get('title'))
            print(request.POST)
            form = RecipeForm(request.POST)
            formset = IngredientFormSet(request.POST)
            form.instance.author = request.user
            if form.is_valid():
                recipe = form.save()
                pk = recipe.id
                formset = IngredientFormSet(request.POST, instance=recipe)
                
                if formset.is_valid():
                    formset.save()
                return redirect("create_recipe_process", pk)
        
    else :
        return render(request, 'recipe/create_recipe.html', {"form" : form, "formset" : formset})



def create_process(request, pk) : 
    Formset_Params = {
    "process_recipe-TOTAL_FORMS" : '1',
    "process_recipe-INITIAL_FORMS" : '0',
    "process_recipe-MIN_NUM_FORMS" : '1', 
    }    
    Formset_Params2 = {
    "cooking_recipe-TOTAL_FORMS" : '1',
    "cooking_recipe-INITIAL_FORMS" : '0',
    "pcooking_recipe-MIN_NUM_FORMS" : '1', 
    }    
    Formset_Params3 = {
    "weight_recipe-TOTAL_FORMS" : '1',
    "weight_recipe-INITIAL_FORMS" : '0',
    "weight_recipe-MIN_NUM_FORMS" : '1', 
    }  
    if request.method ==  "GET":
        print(" GET ")
        recipe_instance = models.Recipe.objects.get(id=pk)
        mainform = RecipeForm( instance=recipe_instance)
#        formset = ProcessFormSet(Formset_Params)
        formset = ProcessFormSet(Formset_Params)
        formset2 = CookingFormSet(Formset_Params2)
        form_weight = WeightFormSet(Formset_Params3)

        return render(request, 'recipe/process.html', {"form" : mainform, "formset" : formset, "formset2" : formset2, "pk":pk, "form_weigths" : form_weight, })
    
    elif request.method == "POST" :
        print(" POST ")
        form = RecipeForm(request.POST)
        #if form.is_valid():
        print(request.POST)
        print(" form is valid ")
        recipe_instance = models.Recipe.objects.get(id=pk)
        formset = ProcessFormSet(request.POST, instance=recipe_instance)
        formset2 = CookingFormSet(request.POST, instance=recipe_instance)
        form_weight = WeightFormSet(request.POST, instance=recipe_instance)
   

        if formset.is_valid():
            print(" form of formset is valid ")
            formset.save()
            
        if formset2.is_valid():
            print(" form of formset is valid ")
            formset2.save()

        if form_weight.is_valid():
            print(" weight form is valid ")
            form_weight.save()
            print(form_weight)

        #else :
            #print(" Form is invalid") 

        if request.user.is_staff :
            return redirect('recettes-recipe-admin')
        else :
            return redirect('recettes-recipe-utilisateur')  
                
    else :
        if request.user.is_staff :
            return redirect('recettes-recipe-admin')
        else :
            return redirect('recettes-recipe-utilisateur')  


            
def update_recipe2(request, pk) : 
    Formset_Params = {
    'ingredients_recipe-TOTAL_FORMS' : '1',
    'ingredients_recipe-INITIAL_FORMS' : '0',
    'ingredients_recipe-MIN_NUM_FORMS' : '1', 
    } 

    recipe_instance = models.Recipe.objects.get(id=pk)   
    if request.method ==  "GET":

        mainform = RecipeForm(instance=recipe_instance)

        if len(models.IngredientRecipe.objects.filter(recipe=recipe_instance)) > 0 :
            formset = IngredientFormSet(instance=recipe_instance)
        else :
            formset = IngredientFormSet(Formset_Params)


        #formset = IngredientFormSet(instance=recipe_instance, )
        #print(formset)
        return render(request, 'recipe/update_recipe.html', {"form" : mainform, "formset" : formset , "pk" : pk})

    elif request.method == "POST" :

        #supprimer les ingrédients actuels
        #models.IngredientRecipe.objects.filter(recipe=recipe_instance).delete() 
        #models.Recipe.objects.get(id=pk)   

        print(request.POST.get('title'))

        form = RecipeForm(request.POST, request.FILES,recipe_instance)
        #form = RecipeForm(request.POST)
        form.instance.author = request.user
        #form.save()
        


        #if form.is_valid():
        #    print(request.POST)
        recipe_instance.title = request.POST.get('title')
        recipe_instance.updated = datetime.now()
        recipe_instance.save(update_fields=['title', 'updated'])


        formset = IngredientFormSet(request.POST, instance=recipe_instance)
        #formset = IngredientFormSet(request.POST)

            
        #if formset.is_valid():
        if formset.is_valid():
            print(" form of formset is valid ")
            formset.save()
        #print(formset)
       
                
        return redirect("update_recipe_process" , pk)
        
    else :
        return render(request, 'recipe/update_recipe.html', {"form" : form})




def update_process(request, pk) : 
    Formset_Params = {
    "process_recipe-TOTAL_FORMS" : '1',
    "process_recipe-INITIAL_FORMS" : '0',
    "process_recipe-MIN_NUM_FORMS" : '1', 
    }    
    Formset_Params2 = {
    "cooking_recipe-TOTAL_FORMS" : '1',
    "cooking_recipe-INITIAL_FORMS" : '0',
    "pcooking_recipe-MIN_NUM_FORMS" : '1', 
    }    
    Formset_Params3 = {
    "weight_recipe-TOTAL_FORMS" : '1',
    "weight_recipe-INITIAL_FORMS" : '0',
    "weight_recipe-MIN_NUM_FORMS" : '1', 
    }  
    recipe_instance = models.Recipe.objects.get(id=pk)
    if request.method ==  "GET":


        #ingredients_instance = models.IngredientRecipe.objects.filter(recipe = recipe_instance)


        mainform = RecipeForm(instance=recipe_instance)
        formset = ProcessFormSet(instance=recipe_instance)
        formset2 = CookingFormSet(instance=recipe_instance)

        if len(models.ProcessRecipe.objects.filter(recipe=recipe_instance)) > 0 :
            formset = ProcessFormSet(instance=recipe_instance)
        else :
            formset = ProcessFormSet(Formset_Params)

        if len(models.CookingRecipe.objects.filter(recipe=recipe_instance)) > 0 :
            formset2 = CookingFormSet(instance=recipe_instance)
        else :
            formset2 = CookingFormSet(Formset_Params2)

        if len(models.WeigthRecipe.objects.filter(recipe=recipe_instance)) > 0 :
            form_weight = WeightFormSet(instance=recipe_instance)
        else :
            form_weight = WeightFormSet(Formset_Params3)
    
            

        



        return render(request, 'recipe/update_process.html', {"form" : mainform, "formset" : formset, "formset2" : formset2,"form_weigths" : form_weight, "pk":pk})
    
    elif request.method == "POST" :
        print(request)
        recipe_instance = models.Recipe.objects.get(id=pk)
        form = RecipeForm(request.POST, recipe_instance)
        #if form.is_valid():
        #    print(request.POST)
        #    print(" form is valid ")
        formset = ProcessFormSet(request.POST, instance=recipe_instance)
        formset2 = CookingFormSet(request.POST, instance=recipe_instance)
        form_weight = WeightFormSet(request.POST, instance=recipe_instance)

        recipe_instance.updated = datetime.now()
        recipe_instance.save(update_fields=['updated'])
        #formset = ProcessFormSet(request.POST)
            
        #if formset.is_valid():

        #formset.save()
        #formset2.save()
        #form_weight.save()
        #else :
        #    print(" Form is invalid") 

        
        if formset.is_valid():
            print(" form of formset is valid ")
            formset.save()
            
        if formset2.is_valid():
            print(" form of formset is valid ")
            formset2.save()

        if form_weight.is_valid():
            print(" weight form is valid ")
            form_weight.save()
            print(form_weight)


        if request.user.is_staff :
            return redirect('recettes-recipe-admin')
        else :
            return redirect('recettes-recipe-utilisateur')  
                
    else :
        if request.user.is_staff :
            return redirect('recettes-recipe-admin')
        else :
            return redirect('recettes-recipe-utilisateur')  







def admin_recipe(request) :
    if request.method == 'GET':
        recipes = models.Recipe.objects.all()
        context = {"recipes" : recipes, "recipes_list" : recipes }
        return render(request, 'recipe/recettes_admin.html', context)

    if request.method == 'POST':
        if request.POST.get("submit_id"):
            pk = request.POST['id']
            recipe_instance = models.Recipe.objects.get(id = pk)

            print(recipe_instance)
            recipe_clone = recipe_instance

            recipe_clone.id = None
            recipe_clone.pk = None
            recipe_clone.title = recipe_instance.title + '_BIS' 
            recipe_clone.save()

            recipe_instance = models.Recipe.objects.get(id = pk)
            ingredients_instance = models.IngredientRecipe.objects.filter(recipe = recipe_instance).order_by('pk')
            for ingredient in ingredients_instance :
                        ingredient_clone = ingredient
                        ingredient_clone.id = None
                        ingredient_clone.pk = None
                        ingredient_clone.recipe = recipe_clone 
                        ingredient_clone.save()    
                        print(ingredient)        

            recipe_instance = models.Recipe.objects.get(id = pk)
            ingredients_instance = models.ProcessRecipe.objects.filter(recipe = recipe_instance).order_by('pk')
            for etape_prep in ingredients_instance :
                        etape_clone = etape_prep
                        etape_clone.id = None
                        etape_clone.pk = None
                        etape_clone.recipe = recipe_clone 
                        etape_clone.save()    
                        print(etape_clone)        


            recipe_instance = models.Recipe.objects.get(id = pk)
            ingredients_instance = models.CookingRecipe.objects.filter(recipe = recipe_instance).order_by('pk')
            for etape_prep in ingredients_instance :
                        etape_clone = etape_prep
                        etape_clone.id = None
                        etape_clone.pk = None
                        etape_clone.recipe = recipe_clone 
                        etape_clone.save()    
                        print(etape_clone)        


            recipe_instance = models.Recipe.objects.get(id = pk)

            if len(models.WeigthRecipe.objects.filter(recipe=recipe_instance)) > 0 :

                weights_instance = models.WeigthRecipe.objects.filter(recipe = recipe_instance)[0]

                weights_clone = weights_instance
                weights_clone.id = None
                weights_clone.pk = None
                weights_clone.recipe = recipe_clone 
                weights_clone.save()    
                #print(weights_clone)        


            recipes = models.Recipe.objects.all()
            context = {"recipes" : recipes, "recipes_list" : recipes}
            return render(request, 'recipe/recettes_admin.html', context)
            #return HttpResponseRedirect(reverse_lazy('recettes-recipe-utilisateur'))

        if request.POST.get("search_button"):
            name_recipe = request.POST['search']
            print(request.POST)
            print(name_recipe)
            print(type(models.Recipe.objects.get(title='recette1').title))
            recipes_list = models.Recipe.objects.all()
            recipes = models.Recipe.objects.all().filter(title  = name_recipe)
            context = {"recipes_list" : recipes_list, "recipes" : recipes }
            return render(request, 'recipe/recettes_admin.html', context)
            #return HttpResponseRedirect(reverse_lazy('recettes-recipe-utilisateur'))



def recipes_view(request):
    if request.method == 'GET':
        recipes = models.Recipe.objects.all()
        context = {"recipes" : recipes, "recipes_list" : recipes, }
        return render(request, 'recipe/recettes.html', context)

    if request.method == 'POST':
        if request.POST.get("submit_id"):
            pk = request.POST['id']
            recipe_instance = models.Recipe.objects.get(id = pk)

            print(recipe_instance)
            recipe_clone = recipe_instance

            recipe_clone.id = None
            recipe_clone.pk = None
            recipe_clone.title = recipe_instance.title + '_BIS' 
            recipe_clone.author = request.user
            recipe_clone.save()


            recipe_instance = models.Recipe.objects.get(id = pk)
            ingredients_instance = models.IngredientRecipe.objects.filter(recipe = recipe_instance).order_by('pk')
            print(ingredients_instance)
            for ingredient in ingredients_instance :
                        ingredient_clone = ingredient
                        ingredient_clone.id = None
                        ingredient_clone.pk = None
                        ingredient_clone.recipe = recipe_clone 
                        ingredient_clone.save()    
                        print(ingredient)        

            recipe_instance = models.Recipe.objects.get(id = pk)
            ingredients_instance = models.ProcessRecipe.objects.filter(recipe = recipe_instance).order_by('pk')
            print(ingredients_instance)
            for etape_prep in ingredients_instance :
                        etape_clone = etape_prep
                        etape_clone.id = None
                        etape_clone.pk = None
                        etape_clone.recipe = recipe_clone 
                        etape_clone.save()    
                        print(etape_clone)        



            recipe_instance = models.Recipe.objects.get(id = pk)
            ingredients_instance = models.CookingRecipe.objects.filter(recipe = recipe_instance).order_by('pk')
            for etape_prep in ingredients_instance :
                        etape_clone = etape_prep
                        etape_clone.id = None
                        etape_clone.pk = None
                        etape_clone.recipe = recipe_clone 
                        etape_clone.save()    
                        print(etape_clone)        


            if len(models.WeigthRecipe.objects.filter(recipe=recipe_instance)) > 0 :            

                recipe_instance = models.Recipe.objects.get(id = pk)
                weights_instance = models.WeigthRecipe.objects.filter(recipe = recipe_instance)[0]
                weights_clone = weights_instance
                weights_clone.id = None
                weights_clone.pk = None
                weights_clone.recipe = recipe_clone 
                weights_clone.save()    
                #print(weights_clone)        



            recipes = models.Recipe.objects.all()
            context = {"recipes" : recipes, "recipes_list" : recipes }
            return render(request, 'recipe/recettes.html', context)

        if request.POST.get("search_button"):
            name_recipe = request.POST['search']
            print(request.POST)
            print(name_recipe)

            recipes_list = models.Recipe.objects.all()
            recipes = models.Recipe.objects.all().filter(title  = name_recipe)
            context = {"recipes_list" : recipes, "recipes" : recipes }
            return render(request, 'recipe/recettes.html', context)


class RecipeDetailView(DetailView):
    model = models.Recipe

    def function_test():
        return "Test Function"
    
    def total_calorie(self) : 
        '''
        Calculer les totaux des différents attributs des ingrédients présents dans la recette. Les stocker dans un dicionnaire
        '''
        ingredients = models.IngredientRecipe.objects.filter(recipe = self.object).order_by('-quantity')
        quantite_total = 0

        total_calorique = 0 
        total_calorique_kcal = 0 
        total_glucide = 0
        total_sodium = 0
        total_sel = 0

        total_proteins = 0 
        total_fibres = 0 
        total_eau= 0
        total_lipide = 0

        total_sucres = 0
        total_fructose = 0 
        total_galactose = 0 
        total_glucose= 0
        total_lactose = 0
        total_maltose= 0 
        total_saccharose = 0 
        total_amidon= 0

        total_fibresAlimentaires = 0
        total_polyols= 0 
        total_cendres = 0 
        total_alcool= 0
        
        total_acidesOrganiques = 0
        total_AGsatures = 0 
        total_AGmonoinsature = 0 
        total_AGpolyinsature = 0
        total_AGbutyrique = 0
        total_AGcaproique = 0 
        total_AGcaprylique = 0 
        total_AGcaprique = 0

        total_AGlaurique = 0 
        total_AGmyristique = 0
        total_AGpalmitique = 0
        total_AGbstearique = 0 
        total_AGoleique = 0 
        
        total_AGlinoleique = 0 
        total_AGalphalinolenique = 0

        total_AGepa = 0
        total_AGdha = 0

        total_cholesterol = 0 
        total_selchlorure = 0
        total_calcium = 0 
        total_cuivre = 0
        total_fer = 0 
        total_iode = 0 
        total_magnesium = 0
        total_manganese = 0
        total_phosphore = 0
        total_potassium= 0 
        total_selenium = 0 
        total_zinc = 0
        total_retinol= 0
        total_betacarotene = 0

        total_vitamineD = 0
        total_vitamineE = 0 
        total_VitamineK1 = 0 
        total_vitamineK2 = 0
        total_vitamineB1 = 0
        total_vitamineB2 = 0 
        total_vitamineB3 = 0
        total_VitamineB5 = 0 
        total_vitamineB6 = 0
        total_VitamineB9 = 0 
        total_vitamineB12 = 0


        total_fibresAlimentaires = 0
        total_sels_ajoutes = 0
        total_sucres_ajoutes = 0

        Total_graisses_ajoutes = 0
        Total_fruitslegumineuse = 0
        Total_eau_ajoutee = 0

        quantite_total = 0.001
        if ingredients.__len__ == 0 :
            quantite_total = 1
            print(ingredients)
            print(" est vide")

        else :
            print(ingredients)
        for ingredient in ingredients : 

            if ingredient.ingredient.forme.name=='sels' :
                total_sels_ajoutes = total_sels_ajoutes + ingredient.quantity 

            if ingredient.ingredient.forme.name=='eaux' :
                Total_eau_ajoutee = Total_eau_ajoutee + ingredient.quantity 

            if ingredient.ingredient.forme.name=='sucres, miels et assimilés' :
                total_sucres_ajoutes = total_sucres_ajoutes + ingredient.quantity 

            if ingredient.ingredient.famille.name =='Matières grasses' :
                Total_graisses_ajoutes = Total_graisses_ajoutes + ingredient.quantity 

            if ingredient.ingredient.famille.name =='Fruits, légumes, légumineuses et oléagineux' :
                Total_fruitslegumineuse = Total_fruitslegumineuse + ingredient.quantity 

        # Quantité d'ingrédients de type eau présente dans la recette 



            if isinstance(ingredient.ingredient.energie_kJ, float):
                total_calorique  = total_calorique + ingredient.quantity * (ingredient.ingredient.energie_kJ)

            if isinstance(ingredient.ingredient.energie_kcal, float):
                total_calorique_kcal  = total_calorique_kcal + ingredient.quantity * (ingredient.ingredient.energie_kcal)
            
            if isinstance(ingredient.ingredient.glucide , float):
                total_glucide  = total_glucide + ingredient.quantity * (ingredient.ingredient.glucide)

            if isinstance(ingredient.ingredient.sodium , float):
                total_sodium  = total_sodium + ingredient.quantity * (ingredient.ingredient.sodium)

            if isinstance(ingredient.ingredient.sodium , float):
                total_sel  = total_sel + ingredient.quantity * (ingredient.ingredient.selchlorure)


            if isinstance(ingredient.ingredient.energie_kJ, float):
                total_proteins  = total_proteins + ingredient.quantity * (ingredient.ingredient.proteins)

            if isinstance(ingredient.ingredient.fibres, float):
                total_fibres  = total_fibres + ingredient.quantity * (ingredient.ingredient.fibres)
            
            if isinstance(ingredient.ingredient.eau , float):
                total_eau  = total_eau + ingredient.quantity * (ingredient.ingredient.eau)

            if isinstance(ingredient.ingredient.lipide , float):
                total_lipide  = total_lipide + ingredient.quantity * (ingredient.ingredient.lipide)



            if isinstance(ingredient.ingredient.sucres, float):
                total_sucres  = total_sucres + ingredient.quantity * (ingredient.ingredient.sucres)

            if isinstance(ingredient.ingredient.fructose, float):
                total_fructose  = total_fructose + ingredient.quantity * (ingredient.ingredient.fructose)
            
            if isinstance(ingredient.ingredient.galactose , float):
                total_galactose  = total_galactose + ingredient.quantity * (ingredient.ingredient.galactose)

            if isinstance(ingredient.ingredient.glucose , float):
                total_glucose  = total_glucose + ingredient.quantity * (ingredient.ingredient.glucose)

            if isinstance(ingredient.ingredient.lactose, float):
                total_lactose  = total_lactose + ingredient.quantity * (ingredient.ingredient.lactose)

            if isinstance(ingredient.ingredient.maltose, float):
                total_maltose  = total_maltose + ingredient.quantity * (ingredient.ingredient.maltose)

            if isinstance(ingredient.ingredient.saccharose, float):
                total_saccharose  = total_saccharose + ingredient.quantity * (ingredient.ingredient.saccharose)
            
            if isinstance(ingredient.ingredient.amidon , float):
                total_amidon  = total_amidon + ingredient.quantity * (ingredient.ingredient.amidon)

            if isinstance(ingredient.ingredient.fibresALimentraires , float):
                total_fibresAlimentaires  = total_fibresAlimentaires + ingredient.quantity * (ingredient.ingredient.fibresALimentraires)

            if isinstance(ingredient.ingredient.polyols, float):
                total_polyols  = total_polyols + ingredient.quantity * (ingredient.ingredient.polyols)


            if isinstance(ingredient.ingredient.cendres , float):
                total_cendres  = total_cendres + ingredient.quantity * (ingredient.ingredient.cendres)

            if isinstance(ingredient.ingredient.alcool , float):
                total_alcool  = total_alcool + ingredient.quantity * (ingredient.ingredient.alcool)

            if isinstance(ingredient.ingredient.acidesOrganiques, float):
                total_acidesOrganiques  = total_acidesOrganiques + ingredient.quantity * (ingredient.ingredient.acidesOrganiques)


            if isinstance(ingredient.ingredient.AGsatures, float):
                total_AGsatures  = total_AGsatures + ingredient.quantity * (ingredient.ingredient.AGsatures)

            if isinstance(ingredient.ingredient.AGmonoinsature, float):
                total_AGmonoinsature  = total_AGmonoinsature + ingredient.quantity * (ingredient.ingredient.AGmonoinsature)

            if isinstance(ingredient.ingredient.AGpolyinsature, float):
                total_AGpolyinsature  = total_AGpolyinsature + ingredient.quantity * (ingredient.ingredient.AGpolyinsature)
            
            if isinstance(ingredient.ingredient.AGbutyrique , float):
                total_AGbutyrique  = total_AGbutyrique + ingredient.quantity * (ingredient.ingredient.AGbutyrique)

            if isinstance(ingredient.ingredient.AGcaproique , float):
                total_AGcaproique  = total_AGcaproique + ingredient.quantity * (ingredient.ingredient.AGcaproique)

            if isinstance(ingredient.ingredient.AGcaprylique, float):
                total_AGcaprylique  = total_AGcaprylique + ingredient.quantity * (ingredient.ingredient.AGcaprylique)

            if isinstance(ingredient.ingredient.AGcaprique , float):
                total_AGcaprique  = total_AGcaprique + ingredient.quantity * (ingredient.ingredient.AGcaprique)

            if isinstance(ingredient.ingredient.AGlaurique , float):
                total_AGlaurique  = total_AGlaurique + ingredient.quantity * (ingredient.ingredient.AGlaurique)

            if isinstance(ingredient.ingredient.AGmyristique, float):
                total_AGmyristique  = total_AGmyristique + ingredient.quantity * (ingredient.ingredient.AGmyristique)

            if isinstance(ingredient.ingredient.AGpalmitique , float):
                total_AGpalmitique  = total_AGpalmitique + ingredient.quantity * (ingredient.ingredient.AGpalmitique)

            if isinstance(ingredient.ingredient.AGbstearique, float):
                total_AGbstearique  = total_AGbstearique + ingredient.quantity * (ingredient.ingredient.AGbstearique)

            if isinstance(ingredient.ingredient.AGoleique , float):
                total_AGoleique  = total_AGoleique + ingredient.quantity * (ingredient.ingredient.AGoleique)

            if isinstance(ingredient.ingredient.AGlinoleique , float):
                total_AGlinoleique  = total_AGlinoleique + ingredient.quantity * (ingredient.ingredient.AGlinoleique)

            if isinstance(ingredient.ingredient.AGalphalinolenique , float):
                total_AGalphalinolenique  = total_AGalphalinolenique + ingredient.quantity * (ingredient.ingredient.sodium)

            if isinstance(ingredient.ingredient.AGepa, float):
                total_AGepa  = total_AGepa + ingredient.quantity * (ingredient.ingredient.AGepa)

            if isinstance(ingredient.ingredient.AGdha, float):
                total_AGdha  = total_AGdha + ingredient.quantity * (ingredient.ingredient.AGdha)

            if isinstance(ingredient.ingredient.cholesterol, float):
                total_cholesterol  = total_cholesterol + ingredient.quantity * (ingredient.ingredient.cholesterol)

            if isinstance(ingredient.ingredient.selchlorure , float):
                total_selchlorure  = total_selchlorure + ingredient.quantity * (ingredient.ingredient.selchlorure)

            if isinstance(ingredient.ingredient.calcium, float):
                total_calcium  = total_calcium + ingredient.quantity * (ingredient.ingredient.calcium)

            if isinstance(ingredient.ingredient.cuivre, float):
                total_cuivre  = total_cuivre + ingredient.quantity * (ingredient.ingredient.cuivre)

            if isinstance(ingredient.ingredient.fer , float):
                total_fer  = total_fer + ingredient.quantity * (ingredient.ingredient.fer)

            if isinstance(ingredient.ingredient.iode , float):
                total_iode  = total_iode + ingredient.quantity * (ingredient.ingredient.iode)

            if isinstance(ingredient.ingredient.magnesium, float):
                total_magnesium  = total_magnesium + ingredient.quantity * (ingredient.ingredient.magnesium)



            if isinstance(ingredient.ingredient.manganese, float):
                total_manganese  = total_manganese + ingredient.quantity * (ingredient.ingredient.manganese)

            if isinstance(ingredient.ingredient.phosphore , float):
                total_phosphore  = total_phosphore + ingredient.quantity * (ingredient.ingredient.phosphore)

            if isinstance(ingredient.ingredient.potassium, float):
                total_potassium  = total_potassium + ingredient.quantity * (ingredient.ingredient.potassium)

            if isinstance(ingredient.ingredient.selenium , float):
                total_selenium  = total_selenium + ingredient.quantity * (ingredient.ingredient.selenium)

            if isinstance(ingredient.ingredient.zinc , float):
                total_zinc  = total_zinc + ingredient.quantity * (ingredient.ingredient.zinc)

            if isinstance(ingredient.ingredient.retinol, float):
                total_retinol  = total_retinol + ingredient.quantity * (ingredient.ingredient.retinol)

            if isinstance(ingredient.ingredient.betaCarotene , float):
                total_betacarotene  = total_betacarotene + ingredient.quantity * (ingredient.ingredient.betaCarotene)

            if isinstance(ingredient.ingredient.vitamineD , float):
                total_vitamineD  = total_vitamineD + ingredient.quantity * (ingredient.ingredient.vitamineD)

            if isinstance(ingredient.ingredient.vitamineE, float):
                total_vitamineE  = total_vitamineE + ingredient.quantity * (ingredient.ingredient.vitamineE)
            if isinstance(ingredient.ingredient.VitamineK1 , float):
                total_VitamineK1  = total_VitamineK1 + ingredient.quantity * (ingredient.ingredient.VitamineK1)

            if isinstance(ingredient.ingredient.vitamineK2 , float):
                total_vitamineK2  = total_vitamineK2 + ingredient.quantity * (ingredient.ingredient.vitamineK2)

            if isinstance(ingredient.ingredient.vitamineB1, float):
                total_vitamineB1  = total_vitamineB1 + ingredient.quantity * (ingredient.ingredient.vitamineB1)

            
            if isinstance(ingredient.ingredient.vitamineB2, float):
                total_vitamineB2  = total_vitamineB2 + ingredient.quantity * (ingredient.ingredient.vitamineB2)

#####vitamineB2

            if isinstance(ingredient.ingredient.VitamineB3 , float):
                total_vitamineB3  = total_vitamineB3 + ingredient.quantity * (ingredient.ingredient.VitamineB3)

            if isinstance(ingredient.ingredient.vitamineB5 , float):
                total_VitamineB5  = total_VitamineB5 + ingredient.quantity * (ingredient.ingredient.vitamineB5)

            if isinstance(ingredient.ingredient.vitamineB9, float):
                total_vitamineB6  = total_vitamineB6 + ingredient.quantity * (ingredient.ingredient.vitamineB6)
            if isinstance(ingredient.ingredient.glucide , float):
                total_VitamineB9  = total_VitamineB9 + ingredient.quantity * (ingredient.ingredient.vitamineB9)
#Changing V to V
            if isinstance(ingredient.ingredient.VitamineB12 , float):
                total_vitamineB12  = total_vitamineB12 + ingredient.quantity * (ingredient.ingredient.VitamineB12)

                
            if isinstance(ingredient.quantity, float):
                quantite_total  = quantite_total + ingredient.quantity 

        #quantite totale sans eau 
        quantite_total = quantite_total - Total_eau_ajoutee


        total_AG_trans = total_AGsatures +  total_AGbutyrique + total_AGcaproique + total_AGcaprylique + total_AGcaprique + total_AGlaurique
        + total_AGmyristique + total_AGpalmitique + total_AGbstearique + total_AGoleique + total_AGlinoleique + total_AGalphalinolenique
        + total_AGepa + total_AGdha

        total_AG_insatures = total_AGmonoinsature + total_AGpolyinsature

        total_AG = total_AG_trans + total_AG_insatures + total_AGsatures
        total_VitamineK = total_VitamineK1 + total_vitamineK2

        return {"total_calorique" : total_calorique / quantite_total, "total_calorique_kcal" : total_calorique_kcal/quantite_total,
                "total_glucide" : total_glucide / quantite_total, "total_sodium" : total_sodium / quantite_total, 
                "total_sel" : total_sel/quantite_total, 
                "total_proteins" : total_proteins / quantite_total, "total_fibres" : total_fibres / quantite_total, 
                "total_eau" : total_eau / quantite_total, "total_sodium" : total_sodium / quantite_total, 
                "total_lipide" : total_lipide / quantite_total, "total_sucres" : total_sucres / quantite_total, 
                "total_fructose" : total_fructose / quantite_total, "total_galactose" : total_galactose / quantite_total, 
                "total_glucose" : total_glucose / quantite_total, "total_lactose" : total_lactose / quantite_total, 
                "total_maltose" : total_maltose / quantite_total, "total_saccharose" : total_saccharose / quantite_total, 
                "total_amidon" : total_amidon / quantite_total, "total_fibresAlimentaires" : total_fibresAlimentaires / quantite_total, 
                "total_polyols" : total_polyols / quantite_total, "total_cendres" : total_cendres / quantite_total, 
                "total_alcool" : total_alcool / quantite_total, "total_acidesOrganiques" : total_acidesOrganiques / quantite_total, 
                "total_AGsatures" : total_AGsatures / quantite_total, "total_AGmonoinsature" : total_AGmonoinsature / quantite_total, 
                "total_AGpolyinsature" : total_AGpolyinsature / quantite_total, "total_AGbutyrique" : total_AGbutyrique / quantite_total, 
                "total_AGcaproique" : total_AGcaproique / quantite_total, "total_AGcaprylique" : total_AGcaprylique / quantite_total, 
                "total_AGcaprique" : total_AGcaprique / quantite_total, "total_AGlaurique" : total_AGlaurique / quantite_total, 
        
                "total_AGmyristique" : total_AGmyristique / quantite_total, "total_AGpalmitique" : total_AGpalmitique / quantite_total, 

                "total_AGbstearique" : total_AGbstearique / quantite_total, "total_AGoleique" : total_AGoleique / quantite_total, 

                "total_AGlinoleique" : total_AGlinoleique / quantite_total, "total_AGalphalinolenique" : total_AGalphalinolenique / quantite_total, 

                        
                "total_AGepa" : total_AGepa / quantite_total, "total_AGdha" : total_AGdha / quantite_total, "total_cholesterol" : total_cholesterol / quantite_total, 

                "total_selchlorure" : total_selchlorure / quantite_total, "total_cuivre" : total_cuivre / quantite_total, 

                "total_fer" : total_fer / quantite_total, "total_iode" : total_iode / quantite_total, 

                "total_magnesium" : total_magnesium / quantite_total, "total_manganese" : total_manganese / quantite_total, "total_calcium" : total_calcium / quantite_total, 

                "total_phosphore" : total_phosphore / quantite_total, "total_potassium" : total_potassium / quantite_total, 

                "total_selenium" : total_selenium / quantite_total, "total_zinc" : total_zinc / quantite_total, 
                
                "total_retinol" : total_retinol / quantite_total, "total_betacarotene" : total_betacarotene / quantite_total, 

                "total_vitamineD" : total_vitamineD / quantite_total, "total_vitamineE" : total_vitamineE / quantite_total, 

                "total_VitamineK1" : total_VitamineK1 / quantite_total, "total_vitamineK2" : total_vitamineK2 / quantite_total, 


                "total_vitamineK" : total_VitamineK1 + total_vitamineK2/ quantite_total, 

                    
                "total_vitamineB1" : total_vitamineB1 / quantite_total, "total_vitamineB2" : total_vitamineB2 / quantite_total, 

                "total_vitamineB3" : total_vitamineB3 / quantite_total, "total_VitamineB5" : total_VitamineB5 / quantite_total, 

                "total_vitamineB6" : total_vitamineB6 / quantite_total, "total_VitamineB9" : total_VitamineB9 / quantite_total,  

                "total_VitamineB12" : total_vitamineB12 / quantite_total,   "total_sels_ajoutes" : total_sels_ajoutes / quantite_total , 
                 
                "total_sucres_ajoutes" : 100*total_sucres_ajoutes / quantite_total, "total_graisses_ajoutes" : 100 * Total_graisses_ajoutes / quantite_total, "total_fruitslegumineuse" : 100 * Total_fruitslegumineuse / quantite_total ,
                "total_AG" : total_AGsatures + total_AGmonoinsature + total_AGpolyinsature , "total_AG_insatures" : total_AGmonoinsature + total_AGpolyinsature, "total_AG_trans" : 0, "Quantite_totale" : quantite_total, "total_eau_ajoutee" : Total_eau_ajoutee}


    def score_calorie_kj(self, total_calorique) : 
        '''Calculer un score selon le total obtenu'''
        arrondi = round( total_calorique,1 )
        if arrondi <= 335 : 
            return 0
        elif arrondi <= 670:
            return 1 
        elif arrondi <= 1005 : 
            return 2
        elif arrondi <= 1340 :
            return 3 
        elif arrondi <= 1675 : 
            return 4
        elif arrondi <= 2010 :
            return 5 
        elif arrondi <= 2345 : 
            return 6
        elif arrondi <= 2680 :
            return 7 
        elif arrondi <= 3015 : 
            return 8
        elif arrondi <= 3350 :
            return 9
        else :
            return 10


    def score_sodium(self, total_sodium) : 

        arrondi = round( total_sodium,2 )
        if arrondi <= 90 : 
            return 0
        elif arrondi <= 180:
            return 1 
        elif arrondi <= 270 : 
            return 2
        elif arrondi <= 360 :
            return 3 
        elif arrondi <= 450 : 
            return 4
        elif arrondi <= 540 :
            return 5 
        elif arrondi <= 630 : 
            return 6
        elif arrondi <= 720 :
            return 7 
        elif arrondi <= 810 : 
            return 8
        elif arrondi <= 900 :
            return 9
        else :
            return 10 

    def score_glucide(self, total_glucide) : 
        ''' Calculer score de glucide '''

        arrondi = round( total_glucide,2)
        if arrondi <= 4.5 : 
            return 0
        elif arrondi <= 9:
            return 1 
        elif arrondi <= 13.5 : 
            return 2
        elif arrondi <= 18 :
            return 3 
        elif arrondi <= 22.5 : 
            return 4
        elif arrondi <= 27 :
            return 5 
        elif arrondi <= 31 : 
            return 6
        elif arrondi <= 36 :
            return 7 
        elif arrondi <= 40 : 
            return 8
        elif arrondi <= 45 :
            return 9
        else :
            return 10

    def score_agsature(self, total_agsature) : 
        ''' Calculer score d'acides gras saturés '''

        arrondi = round( total_agsature,1)
        if arrondi <= 1 : 
            return 0
        elif arrondi <= 2:
            return 1 
        elif arrondi <= 3 : 
            return 2
        elif arrondi <= 4 :
            return 3 
        elif arrondi <= 5 : 
            return 4
        elif arrondi <= 6 :
            return 5 
        elif arrondi <= 7 : 
            return 6
        elif arrondi <= 8 :
            return 7 
        elif arrondi <= 9 : 
            return 8
        elif arrondi <= 10 :
            return 9
        else :
            return 10

    def score_protein(self, total_protein) : 
        ''' Calculer score de protein '''

        arrondi = round( total_protein,2)
        if arrondi <= 1.6 : 
            return 0
        elif arrondi <= 3.2:
            return 1 
        elif arrondi <= 4.8 : 
            return 2
        elif arrondi <= 6.4 :
            return 3 
        elif arrondi <= 8 : 
            return 4
        else :
            return 5

    def score_fibre(self, total_fibre) : 
        ''' Calculer score de fibres '''
        arrondi = round( total_fibre,2)
        if arrondi <= 0.9 : 
            return 0
        elif arrondi <= 1.9:
            return 1 
        elif arrondi <= 2.8 : 
            return 2
        elif arrondi <= 3.7 :
            return 3 
        elif arrondi <= 4.7 : 
            return 4
        else :
            return 5


    def score_fln(self,total_graisse, total_fruitslegumes) : 
        ''' Calculer score de fruit légumes et légumineuse '''
        arrondi = round( total_graisse + total_fruitslegumes ,1)
        if arrondi <= 40 : 
            return 0
        elif arrondi <= 60:
            return 1 
        elif arrondi <= 80 : 
            return 2
        else :
            return 5

    def score_A(self, pts_kj, pts_glucide, pts_agsatures, pts_sodium) : 
        ''' Calculer score A '''
        score =  pts_kj + pts_glucide + pts_agsatures + pts_sodium
        return score

    def nutriscore(self, scoreA, pts_fln, pts_prot, pts_fib):
        ''' Attribuer un nutriscore selon les scores calculés'''
        if (scoreA < 11 and scoreA > 0) or (scoreA >= 11 and pts_fln == 5) : 
            return scoreA - (pts_prot + pts_fln)

        else :
            return scoreA - pts_fln - pts_fib

    def nutriscoreLettre(self, nutriscore):
        if nutriscore < 0 : 
            return "Nutriscore A"
        elif nutriscore < 3 :
            return "Nutriscore B"
        elif nutriscore < 11 :
            return "Nutriscore C"  
        elif nutriscore < 19 :
            return "Nutriscore D"
        else :
            return "Nutriscore E"
    
####################################################################################################################    
#
#           Calcul des allegations 
#
####################################################################################################################
    def allegation(self, total_cal, total_graisse, total_ag_saturee,
     total_ag_trans, total_ag, total_sucres, total_sucres_ajoutes, total_sel, total_sodium, total_sel_ajoute, 
     total_fibre, total_protein, total_graisses_monoinsatures, total_graisses_polyinsatures,
     total_selenium,  total_magnesium, total_phosphore, total_calcium, total_cuivre, total_fer, 
     total_manganese, total_potassium, total_zinc, total_vitamineD, total_vitamineE,
     total_vitamineK, total_vitamineB1,  total_vitamineB2, total_vitamineB3, total_vitamineB5, 
     total_vitamineB6, total_vitamineB9, total_vitamineB12, total_AGepa, total_dha, total_AGalphalinolenique  ) : 
        '''faire une allégation selon les valeurs des différents totaux'''
        allegations = []
        allegations_valeurs = []

        allegations_minerales = []
        allegations_minerales_valeurs = []


        allegations_vitamine_valeurs = []
        allegations_vitamine = []


        if total_cal < 170 : 
            allegations.append('Faible en valeur énergétique' )
            allegations_valeurs.append(round(total_cal, 5))
        elif total_cal < 17 : 
            allegations_valeurs.append(round(total_cal,5))
            allegations.append('Sans apport energetique')

        #ajouter acide gras trans  
        if total_graisse < 3 :
            allegations.append ('faible teneur en matières grasses')
            allegations_valeurs.append(round(total_graisse,5))
        
        elif total_graisse < 0.5 :
            allegations.append ('sans matières grasses' )
            allegations_valeurs.append(round(total_graisse,5))
        
        #à voir avec le client    
        if total_ag_saturee + total_ag_trans < 1.5 :
            allegations.append ('faible teneur en graisses saturees')
            allegations_valeurs.append(round(total_ag_saturee + total_ag_trans,5))

        elif total_ag_saturee + total_ag_trans < 0.1 :
            allegations.append ('faible teneur en graisses saturees')    
            allegations_valeurs.append(round(total_ag_saturee + total_ag_trans,5))
        
        if total_sucres_ajoutes < 5 :
            allegations.append ('faible teneur en sucres')
            allegations_valeurs.append(round(total_sucres_ajoutes,5))

        elif total_sucres_ajoutes < 0.5 :
            allegations.append ('sans sucres')
            allegations_valeurs.append(round(total_sucres_ajoutes,5))
        
        if total_sucres_ajoutes < 2 :
            allegations.append ('Sans sucre ajouté')
            allegations_valeurs.append(round(total_sucres_ajoutes,5))

        #à voir avec le client 
        #if total_sucres_ajoutes < 0.5 :
        #    allegations.append ({'sans sucres ajoutes' : total_sucres})    
        
        if total_sel + total_sodium < 0.12 :
            allegations.append ('pauvre en sel')
            allegations_valeurs.append(round(total_sel + total_sodium,5))   

        elif total_sel + total_sodium < 0.04 :
            allegations.append ('tres pauvre en sel') 
            allegations_valeurs.append(round(total_sel + total_sodium, 5)) 
        
        elif total_sel + total_sodium < 0.005 :
            allegations.append ('sans sodium')  
            allegations_valeurs.append(round(total_sel + total_sodium, 5)) 

        if total_sel_ajoute < 0.005 :
            allegations.append ('sans sodium ou sel ajouté') 
            allegations_valeurs.append(round(total_sel_ajoute,5))  

        #a voir avec le client
        if total_fibre > 3 :
            allegations.append ('source de fibres')  
            allegations_valeurs.append(round(total_fibre,5))   

        elif total_fibre > 6 :
            allegations.append ('riche en fibres')
            allegations_valeurs.append(round(total_fibre),5) 

        #a voir avec le client
        if total_cal > 0 : 
            if total_protein * 4 / total_cal > 0.12 :
                allegations.append ('source de proteins')
                allegations_valeurs.append(round(total_protein * 4 / total_cal,5)) 

            elif total_protein * 4 / total_cal > 0.20 :
                allegations.append ('riche en proteins')
                allegations_valeurs.append(round(total_protein * 4 / total_cal,5)) 
    


        ### 22, 23, 24 
        if (total_AGepa + total_dha > 40) : 
            allegations.append ('source d acide gras omega3')
            allegations_valeurs.append(round(total_AGepa + total_dha,5))

        elif total_AGalphalinolenique > 0.3 : 
            allegations.append ('source d acide gras omega3')
            allegations_valeurs.append(round(total_AGepa + total_dha,5))

        elif (total_AGepa + total_dha > 80) : 
            allegations.append ('riche en acide gras omega3')
            allegations_valeurs.append(round(total_AGepa + total_dha,5))

        elif total_AGalphalinolenique > 0.6 : 
            allegations.append ('riche en acide gras omega3')
            allegations_valeurs.append(round(total_AGalphalinolenique,5))

        total_acide_gras = total_graisses_monoinsatures + total_graisses_polyinsatures + total_ag_saturee

        if total_acide_gras > 0 :
            if total_graisse == 0:
                total_graisse = 1

            if (total_graisses_monoinsatures / total_graisse > 0.45 and total_graisses_monoinsatures * 9 > 0.2 * total_cal) : 
                allegations.append ('riche en graisse monoinsaturees')
                allegations_valeurs.append(round(total_graisses_monoinsatures / total_graisse,5))

            if (total_graisses_polyinsatures / total_graisse  > 0.45 and total_graisses_polyinsatures * 9> 0.2 * total_cal) : 
                allegations.append ('riche en graisse polyinsaturees')
                allegations_valeurs.append(round(total_graisses_monoinsatures / total_graisse,5))

            if ( total_graisses_polyinsatures + total_graisses_monoinsatures / total_graisse > 0.7  and total_graisses_polyinsatures + total_graisses_monoinsatures * 9 > 0.2 * total_cal) : 
                allegations.append ('riche en graisse insaturees')
                allegations_valeurs.append(round(total_graisses_monoinsatures / total_graisse,5))

#########################################################################################33
#
#       Minéraux
#
######################################################################################
        if total_selenium > 8.25 : 
            allegations_minerales.append('source de selenium')
            allegations_minerales_valeurs.append(round(total_selenium,5))
        elif total_selenium > 16.5 : 
            allegations_minerales.append('riche en selenium')
            allegations_minerales_valeurs.append(round(total_selenium,5))            

        if total_magnesium > 0.056 : 
            allegations_minerales.append('source de magnesium')
            allegations_minerales_valeurs.append(round(total_magnesium,5))
        elif total_magnesium > 0.112 : 
            allegations_minerales.append('riche en magnesium')
            allegations_minerales_valeurs.append(round(total_magnesium,5))

        if total_phosphore > 0.105 : 
            allegations_minerales.append('source de phosphore')
            allegations_minerales_valeurs.append(round(total_phosphore,5))

        elif total_phosphore > 0.210 : 
            allegations_minerales.append('riche en phosphore')
            allegations_minerales_valeurs.append(round(total_phosphore,5))

        if total_calcium > 120 : 
            allegations_minerales.append('source de calcium')
            allegations_minerales_valeurs.append(round(total_calcium,5))
        elif total_calcium > 240 : 
            allegations_minerales.append('riche en selenium')
            allegations_minerales_valeurs.append(round(total_calcium,5))

        if total_cuivre > 0.15 : 
            allegations_minerales.append('source de cuivre')
            allegations_minerales_valeurs.append(round(total_cuivre,5))
        elif total_cuivre > 0.30 : 
            allegations_minerales.append('riche en cuivre')
            allegations_minerales_valeurs.append(round(total_cuivre,5))

        if total_fer > 2.1 : 
            allegations_minerales.append('source de fer')
            allegations_minerales_valeurs.append(round(total_fer,5))
        elif total_fer > 4.2 : 
            allegations_minerales.append('riche en fer')
            allegations_minerales_valeurs.append(round(total_fer,5))

        if total_manganese > 0.3 : 
            allegations_minerales.append('source de manganese')
            allegations_minerales_valeurs.append(round(total_manganese,5))
        elif total_manganese > 0.6 : 
            allegations_minerales.append('riche en manganese')
            allegations_minerales_valeurs.append(round(total_manganese,5))

        if total_potassium > 300 : 
            allegations_minerales.append('source de potassium')
            allegations_minerales_valeurs.append(round(total_potassium,5))
        elif total_potassium > 600 : 
            allegations_minerales.append('riche en potassium')    
            allegations_minerales_valeurs.append(round(total_potassium,5))

        if total_zinc > 1.5 : 
            allegations_minerales.append('source de zinc')
            allegations_minerales_valeurs.append(round(total_zinc,5))
        elif total_zinc > 3 : 
            allegations_minerales.append('riche en zinc')
            allegations_minerales_valeurs.append(round(total_zinc,5))

#############################################################
#
#
#####################################################################

        if total_vitamineD > 0.75 : 
            allegations_vitamine.append('source de vitamine D')
            allegations_vitamine_valeurs.append(round(total_vitamineD,5))
        elif total_vitamineD > 1.5 : 
            allegations_vitamine.append('riche en vitamine D')
            allegations_vitamine_valeurs.append(round(total_vitamineD,5))

        if total_vitamineE > 1.8 : 
            allegations_vitamine.append('source de vitamine E')
            allegations_vitamine_valeurs.append(round(total_vitamineE,5))
        elif total_vitamineE > 1.8 : 
            allegations_vitamine.append('riche en vitamine E')
            allegations_vitamine_valeurs.append(round(total_vitamineE,5))
            
        if total_vitamineK > 1.8 : 
            allegations_vitamine.append('source de vitamine K')
            allegations_vitamine_valeurs.append(round(total_vitamineK,5))
        elif total_vitamineK > 1.8 : 
            allegations_vitamine.append('riche en vitamine K')
            allegations_vitamine_valeurs.append(round(total_vitamineK,5))            
            
        if total_vitamineB1 > 0.165 : 
            allegations_vitamine.append('source de vitamine B1')
            allegations_vitamine_valeurs.append(round(total_vitamineB1,5))
        elif total_vitamineB1 > 0.33 : 
            allegations_vitamine.append('riche en vitamine B1')     
            allegations_vitamine_valeurs.append(round(total_vitamineB1,5))

        if total_vitamineB2 > 0.21 : 
            allegations_vitamine.append('source de vitamine B2')
            allegations_vitamine_valeurs.append(round(total_vitamineB2,5))
        elif total_vitamineB2 > 0.42 : 
            allegations_vitamine.append('riche en vitamine B2') 
            allegations_vitamine_valeurs.append(round(total_vitamineB2,5))    


        if total_vitamineB3 > 2.4 : 
            allegations_vitamine.append('source de vitamine B2')
            allegations_vitamine_valeurs.append(round(total_vitamineB3,5))
        elif total_vitamineB3 > 4.2 : 
            allegations_vitamine.append('riche en vitamine B2') 
            allegations_vitamine_valeurs.append(round(total_vitamineB3,5))    

        if total_vitamineB5 > 0.9 : 
            allegations_vitamine.append('source de vitamine B5')
            allegations_vitamine_valeurs.append(round(total_vitamineB5,5))
        elif total_vitamineB5 > 1.8 : 
            allegations_vitamine.append('riche en vitamine B5')  
            allegations_vitamine_valeurs.append(round(total_vitamineB5,5))   

        if total_vitamineB6 > 0.21 : 
            allegations_vitamine.append('source de vitamine B6')
            allegations_vitamine_valeurs.append(round(total_vitamineB6,5))
        elif total_vitamineB6 > 0.42 : 
            allegations_vitamine.append('riche en vitamine B6')
            allegations_vitamine_valeurs.append(round(total_vitamineB6,5))

        if total_vitamineB9 > 30 : 
            allegations_vitamine.append('source de vitamine B9')
            allegations_vitamine_valeurs.append(round(total_vitamineB9,5))
        elif total_vitamineB9 > 60 : 
            allegations_vitamine.append('riche en vitamine B9')
            allegations_vitamine_valeurs.append(round(total_vitamineB9,5))

        if total_vitamineB12 > 0.375 : 
            allegations_vitamine.append('source de vitamine B12')
            allegations_vitamine_valeurs.append(round(total_vitamineB12,5))
        elif total_vitamineB12 > 0.75: 
            allegations_vitamine.append('riche en vitamine B12')
            allegations_vitamine_valeurs.append(round(total_vitamineB12,5))

        return allegations, allegations_minerales, allegations_vitamine, allegations_valeurs, allegations_minerales_valeurs, allegations_vitamine_valeurs


    def get_context_data(self, **kwargs):

        nutriscore_couleur = {"Nutriscore A" : "rgb(0, 128, 0)", "Nutriscore B" : "rgb(0, 255, 0)", "Nutriscore C" : "Yellow", "Nutriscore D" : "#FFA500", "Nutriscore E" : "#FF4500", }

        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        #context['ingredients'] = models.IngredientRecipe.objects.all()

        #Calculer score fln
        ingredient_Recipe = models.IngredientRecipe.objects.filter(recipe = self.object).order_by('-quantity')
        process_Recipe = models.ProcessRecipe.objects.filter(recipe = self.object)
        cooking_Recipe = models.CookingRecipe.objects.filter(recipe = self.object)

        poids_unitaire = 12.5
        poids_cru_unitaire = 12.5

        if len(models.WeigthRecipe.objects.filter(recipe = self.object)) > 0 :
            weight_Recipe = models.WeigthRecipe.objects.filter(recipe = self.object)[0]

            poids_unitaire = weight_Recipe.unitaire
            poids_cru_unitaire = weight_Recipe.cru
            context['poids_unitaire'] = poids_unitaire
            context['poids_cru'] = poids_cru_unitaire
            
        else :
            context['poids_unitaire'] = poids_unitaire
            context['poids_cru'] = poids_cru_unitaire



        '''for i in range(len(ingredient_Recipe)) : 
            if ingredient_Recipe[i].recipe.famille == models.Famille.objects.get(name = 'viandes, œufs, poissons et assimilés'):
                score_fln = score_fln + ingredient_Recipe[i].quantity
        '''



        context['ingredients'] = ingredient_Recipe
        context['process'] = process_Recipe
        context['cooking'] = cooking_Recipe



        totaux = self.total_calorie()

        # Pourcentage après cuisson        
        q_total = totaux["Quantite_totale"]
        perc = []
        if q_total > 0 :
            for i in range (len(ingredient_Recipe)) :
                perc.append( round(ingredient_Recipe[i].quantity / q_total * 100,2)) 
        
        else :
            perc = [0 for i in len(ingredient_Recipe)]        
        context['perc_ingredients'] = perc


        # Pourcentage avant cuisson        
        q_total_eau = totaux["Quantite_totale"] + totaux['total_eau_ajoutee']
        perc_eau = []
        if q_total_eau > 0 :
            for i in range (len(ingredient_Recipe)) :
                perc_eau.append( round(ingredient_Recipe[i].quantity / q_total_eau * 100,2)) 
        
        else :
            perc_eau = [0 for i in len(ingredient_Recipe)]        
        context['perc_ingredients_eau'] = perc_eau



###########################################################################################
#
#   Envoi des quantites calculees au front end
#
############################################################################################


        
        context['quantite_totale'] = round (totaux["Quantite_totale"], 5)
        context['inv_quantite_totale'] = 1/totaux["Quantite_totale"]



        context['total_glucide'] = round(totaux["total_glucide"],5)
        context['total_sodium'] = round (totaux["total_sodium"], 5)

        context['total_protein'] = round (totaux['total_proteins'], 5)
        context['total_fibre'] = round(totaux["total_fibres"],5)
        context['total_eau'] = round(totaux["total_eau"],5)
        context['total_lipide'] = round(totaux["total_lipide"],5)

        context['total_sucres'] = round (totaux['total_sucres'], 5)
        context['total_fructose'] = round(totaux["total_fructose"],5)
        context['total_galactose'] = round(totaux["total_galactose"],5)
        context['total_glucose'] = round(totaux["total_glucose"],5)
        context['total_lactose'] = round (totaux['total_lactose'], 5)
        context['total_maltose'] = round(totaux["total_maltose"],5)
        context['total_saccharose'] = round(totaux["total_saccharose"],5)
        context['total_amidon'] = round(totaux["total_amidon"],5)
        context['total_fibresAlimentaires'] = round(totaux["total_fibresAlimentaires"],5)

        context['total_polyols'] = round(totaux['total_polyols'],5)
        context['total_cendres'] = round(totaux["total_cendres"],5)
        context['total_alcool'] = round(totaux["total_alcool"],5)
        context['total_acidesOrganiques'] = round(totaux["total_acidesOrganiques"],5)
        context['total_AGsatures'] = round(totaux['total_AGsatures'],5)
        context['total_AGmonoinsature'] = round(totaux["total_AGmonoinsature"],5)
        context['total_AGpolyinsature'] = round(totaux["total_AGpolyinsature"],5)
        context['total_AGbutyrique'] = round(totaux["total_AGbutyrique"],5)
        context['total_AGcaproique'] = round(totaux["total_AGcaproique"],5)
        context['total_AGcaprylique'] = round (totaux['total_AGcaprylique'], 5)

        context['total_AGlaurique'] = round(totaux["total_AGlaurique"],5)
        context['total_AGmyristique'] = round(totaux["total_AGmyristique"],5)
        context['total_AGbutyrique'] = round(totaux["total_AGbutyrique"],5)
        context['total_AGpalmitique'] = round(totaux["total_AGpalmitique"],5)
        context['total_AGbstearique'] = round(totaux["total_AGbstearique"],5)
        context['total_AGoleique'] = round(totaux["total_AGoleique"],5)
        context['total_AGlinoleique'] = round(totaux["total_AGlinoleique"],5)
        context['total_AGalphalinolenique'] = round(totaux["total_AGalphalinolenique"],5)

        context['total_AGepa'] = round(totaux["total_AGepa"],5)
        context['total_AGdha'] = round(totaux["total_AGdha"],5)

        context['total_cholesterol'] = round(totaux["total_cholesterol"],5)
        context['total_selchlorure'] = round(totaux["total_selchlorure"],5)
        context['total_calcium'] = round(totaux["total_calcium"],5)
        context['total_cuivre'] = round(totaux["total_cuivre"],5)
        context['total_fer'] = round(totaux["total_fer"],5)
        context['total_iode'] = round (totaux['total_iode'], 5)
        context['total_magnesium'] = round(totaux["total_magnesium"],5)
        context['total_manganese'] = round(totaux["total_manganese"],5)
        context['total_phosphore'] = round(totaux["total_phosphore"],5)
        context['total_potassium'] = round(totaux["total_potassium"],5)
        context['total_selenium'] = round(totaux["total_selenium"],5)
        context['total_zinc'] = round(totaux["total_zinc"],5)
        context['total_retinol'] = round(totaux["total_retinol"],5)
        context['total_betacarotene'] = round(totaux["total_betacarotene"],5)
    


        context['total_VitamineK1'] = round(totaux["total_VitamineK1"],5)
        context['total_vitamineK2'] = round (totaux["total_vitamineK2"], 5)

        context['total_vitamineE'] = round (totaux["total_vitamineE"], 5)
        context['total_vitamineB1'] = round (totaux['total_vitamineB1'], 5)
        context['total_vitamineB2'] = round (totaux["total_vitamineB2"], 5)
        context['total_vitamineB3'] = round(totaux["total_vitamineB3"],5)
    
        context['total_VitamineB5'] = round(totaux['total_VitamineB5'], 5)
        context['total_VitamineB9'] = round (totaux["total_VitamineB9"], 5)
        context['total_VitamineB12'] = round(totaux["total_VitamineB12"],5)
    

        context['total_sels_ajoutes'] = round (totaux['total_sels_ajoutes'], 5)
        context['total_sucres_ajoutes'] = round (totaux["total_sucres_ajoutes"],5)
        context['Total_graisses_ajoutes'] = round(totaux['total_graisses_ajoutes'], 5)
        context['Total_fruitslegumineuse'] = round (totaux["total_fruitslegumineuse"], 5)

        context['total_fln'] = round(totaux['total_graisses_ajoutes'] + totaux["total_fruitslegumineuse"], 5)
        #get the total_fln quantite des ingredients appartenant a fruits, légumes ou légumineuses
        #context['total_fln'] = totaux['total_protein']


        #en kcal
        context['total_calorie_kcal'] = round( 4* totaux["total_glucide"] + 4* totaux['total_proteins'] + 9* totaux["total_lipide"], 2)

        #en kj 
        context['total_calorie'] = round(context['total_calorie_kcal']  * 4.18, 2)


        context['Total_fln'] = round (totaux["total_graisses_ajoutes"] + totaux["total_fruitslegumineuse"], 5)



#######################################################################################################################################
#
# Nutrition Fact per biscuit
#
######################################################################################################################################


        quantite_total = totaux['Quantite_totale']

        context['total_calorie_kcal_bis'] = round (context['total_calorie_kcal'] / 100 * poids_unitaire, 2)
        context['total_calorie_bis'] = round( context['total_calorie'] / 100 * poids_unitaire, 2) 

        context['total_calorie_kcal_gda'] = round (context['total_calorie_kcal_bis'] / 2000 *100, 2)
        context['total_calorie_gda'] = round ( context['total_calorie'] / 8400 * 100, 2)



        context['total_protein_nf'] = round (totaux['total_proteins'] , 2)
        context['total_protein_bis'] = round (totaux['total_proteins'] / 100 * poids_unitaire, 2)
        context['total_protein_gda'] = round (context['total_protein_bis'] / 50 * 100, 2)


        context['total_glucide_nf'] = round (totaux['total_glucide'],  2) 
        context['total_sucres_nf'] = round (totaux['total_sucres'], 2)
        context['total_glucide_bis'] = round (totaux['total_glucide'] / 100 * poids_unitaire, 2) 
        context['total_sucres_bis'] = round (totaux['total_sucres'] / 100 * poids_unitaire, 2)

        context['total_glucide_gda'] =  round (context['total_glucide_bis'] / 260 * 100, 2)
        context['total_sucres_gda'] =  round (context['total_sucres_bis'] / 90 * 100, 2)




        context['total_lipide_nf'] = round (totaux['total_lipide'], 2)
        context['total_AGsatures_nf'] = round(totaux['total_AGsatures'], 2)

        context['total_lipide_bis'] = round (totaux['total_lipide'] / 100 * poids_unitaire, 2)
        context['total_AGsatures_bis'] = round(totaux['total_AGsatures'] / 100 * poids_unitaire, 2)

        context['total_lipide_gda'] = round (context['total_lipide_bis'] / 70 * 100, 2)
        context['total_AGsatures_gda'] = round (context['total_AGsatures_bis'] / 20 * 100, 2)



        context['total_fibre_nf'] = round (totaux['total_fibres'] , 2)
        context['total_fibre_bis'] = round (totaux['total_fibres'] / 100 * poids_unitaire, 2)
        context['total_fibre_gda'] = round (context['total_fibre_bis'] / 25 * 100, 2)

        context['total_sels_ajoutes_nf'] = round (totaux['total_sels_ajoutes'], 2)
        context['total_sodium_bis'] = round (totaux["total_sels_ajoutes"] / 100 * poids_unitaire, 2)
        context['total_sodium_gda'] = round (context["total_sodium_bis"] / 2.4 * 100, 2)



#######################################################################################################################################
#
# Nutrition Fact GDA
#
######################################################################################################################################




        score_kj = self.score_calorie_kj(totaux["total_calorique"])
        score_sodium = self.score_sodium(totaux["total_sodium"])
        score_glucide = self.score_glucide(totaux['total_sucres'])
        score_agsatures = self.score_agsature(totaux["total_AGsatures"])
        score_protein = self.score_protein(totaux["total_proteins"])
        score_fibre = self.score_fibre(totaux["total_fibres"])
        score_fln = self.score_fln(totaux["total_graisses_ajoutes"], totaux["total_fruitslegumineuse"])

        scoreA = self.score_A(score_kj, score_glucide, score_agsatures, score_sodium)
        nutriscore = self.nutriscore(scoreA, score_fln, score_protein, score_fibre)  

        context['Score_sodium'] = score_sodium
        context['Score_kj'] = score_kj
        context['Score_glucide'] = score_glucide
        context['score_AGsatures'] = score_agsatures
        context['score_protein'] = score_protein
        context['score_fibre'] = score_fibre
        context['score_fln'] = score_fln
        context['score_A'] = scoreA
        #context['Score_calorie_kcal'] = 0        

        context['s'] = "rgba(95, 146, 48, 0.815)"

        context['nutriscore'] = self.nutriscoreLettre(nutriscore)
        context['couleur'] = nutriscore_couleur[context['nutriscore']]
        context['allegation'],context['allegation_minerales'],context['allegation_vitamine'], context['allegation_valeurs'], context['allegation_minerales_valeurs'], context['allegation_vitamine_valeurs'] = self.allegation(totaux["total_calorique"], totaux["total_graisses_ajoutes"], totaux["total_AGsatures"], totaux["total_AG_trans"],  totaux["total_AG"], totaux["total_sucres"],
                                totaux["total_sucres_ajoutes"], totaux["total_sel"], totaux["total_sodium"], totaux["total_sels_ajoutes"], totaux["total_fibres"], totaux["total_proteins"], totaux["total_AGmonoinsature"], totaux["total_AGpolyinsature"], 
                                totaux["total_selenium"], totaux["total_magnesium"], totaux["total_phosphore"], totaux["total_calcium"], totaux["total_cuivre"], totaux["total_fer"], totaux["total_manganese"], totaux["total_potassium"], totaux["total_zinc"], 
                                totaux["total_vitamineD"], totaux["total_vitamineE"], totaux["total_VitamineK1"] + totaux["total_vitamineK2"], totaux["total_vitamineB1"],  totaux["total_vitamineB2"], totaux["total_vitamineB3"], totaux["total_VitamineB5"], totaux["total_vitamineB6"], totaux["total_VitamineB9"],
                                totaux["total_VitamineB12"], totaux["total_AGepa"], totaux["total_AGdha"], totaux["total_AGalphalinolenique"] )

    
        return context



    
class RecipeCreateView(CreateView):
    model = models.Recipe
    fields = ['title', 'description', 'cook_time']

    def get_success_url(self):
        if self.request.user.is_staff :
            return reverse_lazy('recettes-recipe-admin')
        else :
            return reverse_lazy('recettes-recipe-utilisateur')  

    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
#class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):


#def RecipeDeleteViewUser(request, pk) :
#    return render(request, "recipe/home.html", context)

#def RecipeDeleteViewAdmin(request, pk) :
#    return redirect("recettes-delete-admin")

    
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Recipe
    #if request.get_user().is_staff :
    #    success_url = reverse_lazy('recettes-recipe-admin')
    #else :
    #    success_url = reverse_lazy('recettes-recipe-utilisateur')

    success_url = reverse_lazy('recettes-recipe-admin')
    print(request)


    def get_success_url(self):
        if self.request.user.is_staff :
            return reverse_lazy('recettes-recipe-admin')
        else :
            return reverse_lazy('recettes-recipe-utilisateur')  

    #def test_func(self):
    #    recipe = self.get_object()
    #    return self.request.user == recipe.author
    
    def test_func(self):
        recipe = self.get_object()
        return True
    
#class RecipeDeleteView2(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#    model = models.Recipe
#    success_url = reverse_lazy('recettes-recipe-utilisateur')
#    template_name = 'recipe_confirm_delete_user.html'

    #def test_func(self):
    #    recipe = self.get_object()
    #    return self.request.user == recipe.author
    
#    def test_func(self):
#        recipe = self.get_object()
#        return True
    
    
    
''' LES INGREDIENTS'''
#class IngredientListView(ListView):
#    model = models.Ingredient 
#    template_name = 'ingredients/ingredients.html'
#    context_object_name = 'ingredients_app'
#    paginate_by = 100

def Ingredient_view(request):
    if request.method == 'GET':
        ingredients = models.Ingredient.objects.all().order_by('name')
        ingredients_list = models.Ingredient.objects.all().order_by('name')
        context = {'ingredients': ingredients, 'ingredients_list': ingredients_list}
        return render(request, 'ingredients/ingredients.html', context)

    if request.method == 'POST':
        if request.POST.get("search_button"):
            name_ingredient = request.POST['search']
            #print(request.POST['search'])
            ingredients_list = models.Ingredient.objects.all()
            ingredients = models.Ingredient.objects.all().filter(name  = name_ingredient)
            context = {"ingredients_list" : ingredients_list, "ingredients" : ingredients }


        
        if request.POST.get("submit_id"):
            ingredients = models.Ingredient.objects.all().order_by('name')
            pk = request.POST['id']
            ingredient_instance = models.Ingredient.objects.get(id = pk)
            ingredient_clone = ingredient_instance

            ingredient_clone.id = None
            ingredient_clone.pk = None
            ingredient_clone.name = ingredient_instance.name + '_BIS' 
            ingredient_clone.save()
            context = {"ingredients_list" : ingredients, "ingredients" : ingredients }      
           
    
        return render(request, 'ingredients/ingredients.html', context)


class IngredientDetailView(DetailView):
    model = models.Ingredient
    template_name = 'ingredients/ingredient_detail.html'
    
class IngredientCreateView(CreateView):
    model = models.Ingredient
    template_name = 'ingredients/ingredient_form.html'
    fields = '__all__'
    success_url = reverse_lazy('ingredients-recipe')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class IngredientUpdateView(UpdateView):
    model = models.Ingredient
    template_name = 'ingredients/ingredient_form.html'
    fields = '__all__'
    success_url = reverse_lazy('ingredients-recipe')

    
class IngredientDeleteView(DeleteView):
    model = models.Ingredient
    template_name = 'ingredients/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredients-recipe')
    
    

    '''def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author'''

    
    
    
''' Les familles'''
class FamilleListView(ListView):
    model = models.Famille 
    template_name = 'familles/familles.html'
    context_object_name = 'familles_app'
    paginate_by = 100

def Famille_view(request):
    if request.method == 'GET':
        familles = models.Famille.objects.all().order_by('name')
        context = {'familles': familles, 'familles_list':familles}
        return render(request, 'familles/familles.html', context)

    if request.method == 'POST':
        if request.POST.get("search_button"):
            name_famille = request.POST['search']
            #print(request.POST['search'])
            familles = models.Famille.objects.all().filter(name  = name_famille)
            context = {"familles_list" : familles, "familles" : familles }
            return render(request, 'familles/familles.html', context)

            
    if request.POST.get("submit_id"):
            familles = models.Famille.objects.all().order_by('name')
            pk = request.POST['id']
            famille_instance = models.Famille.objects.get(id = pk)
            famille_clone = famille_instance

            famille_clone.id = None
            famille_clone.pk = None
            famille_clone.name = famille_instance.name + '_BIS' 
            famille_clone.save()

            context = {"familles_list" : familles, "familles" : familles }      
            return HttpResponseRedirect(reverse_lazy('familles-recipe'))


    return render(request, 'familles/familles.html', context = context)

def Famille_ingredients(request, pk):
    if request.method == 'GET':
        famille = models.Famille.objects.filter(id = pk)[0]
        ingredients = models.Ingredient.objects.filter(famille = famille).order_by('name')
        context = { 'famille' : famille, 'ingredients' : ingredients, 'ingredients_list' : ingredients}
        return render (request, 'familles/famille_ingredient.html', context = context)

    if request.method == 'POST':
        if request.POST.get("search_button"):
            name_ingredient = request.POST['search']
            #print(request.POST['search'])
            ingredients_list = models.Ingredient.objects.all()
            ingredients = models.Ingredient.objects.all().filter(name  = name_ingredient)
            context = {"ingredients_list" : ingredients_list, "ingredients" : ingredients }


        
        if request.POST.get("submit_id"):
            ingredients = models.Ingredient.objects.all().order_by('name')
            pk = request.POST['id']
            ingredient_instance = models.Ingredient.objects.get(id = pk)
            ingredient_clone = ingredient_instance

            ingredient_clone.id = None
            ingredient_clone.pk = None
            ingredient_clone.name = ingredient_instance.name + '_BIS' 
            ingredient_clone.save()
            context = {"ingredients_list" : ingredients, "ingredients" : ingredients }      
           
    
        return render(request, 'ingredients/ingredients.html', context)

class FamilleDetailView(DetailView):
    model = models.Famille
    template_name = 'familles/famille_detail.html'
    
class FamilleCreateView(CreateView):
    model = models.Famille
    template_name = 'familles/famille_form.html'
    fields = '__all__'
    success_url = reverse_lazy('familles-recipe')
    
    #def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)
    
    #def get_success_url(self):
    #    return redirect('familles-recipe')

class FamilleUpdateView(UpdateView):
    model = models.Famille
    template_name = 'familles/famille_form.html'
    fields = '__all__'
    success_url = reverse_lazy('familles-recipe')

    
class FamilleDeleteView(DeleteView):
    model = models.Famille
    template_name = 'familles/famille_confirm_delete.html'
    success_url = reverse_lazy('familles-recipe')
    
    

    '''def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author'''



def test_cascade(request):
    ingredientsObj = models.Ingredient.objects.all()
    famillesObj = models.Famille.objects.all()
    context  = { 'familles' : famillesObj,'ingredients' : ingredientsObj}
    return render(request, 'recipe/test_cascade.html', context)


def ingredient_create_view(request):
    form = IngredientForm()
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_add')
    return render(request, 'recipe/test_cascade.html', {'form': form})

# AJAX
def load_ingredient(request):
    print(request)
    forme_id = request.GET.get('forme_id')
    print("forme_id", forme_id)
    forme = models.Forme.objects.get(id = forme_id)
    print("forme", forme)
    ingredients = forme.forme_ingredient.all().order_by('name')
    print("ingredients", ingredients)
    return render(request, 'recipe/ingredient_dropdown_list_options.html', {'ingredients_famille': ingredients})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

def load_forme(request):
    famille_id = request.GET.get('famille_id')
    famille = models.Famille.objects.get(pk = famille_id)
    formes = famille.forme_famille.all().order_by('name')
    return render(request, 'recipe/forme_dropdown_list_options.html', {'formes_famille': formes})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def duplicate_recipe(request, pk) :  
    if request.method ==  "POST":
        recipe_instance = models.Recipe.objects.get(id=pk)
        recipe_clone = recipe_instance

        recipe_clone.id = None
        recipe_clone.pk = None
        recipe_clone.title = 'clone' 

        recipes = models.Recipe.objects.all()
        context = {"recipes" : recipes }
        return render(request, 'recipe/recettes_admin.html', context)

    
    #elif request.method == "POST" :                
    #    return redirect("recettes-recipe")
    #else :
    #    return redirect("recettes-recipe" )


    