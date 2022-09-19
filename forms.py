from django import forms
from .models import Famille, Forme, Ingredient, IngredientRecipe, Recipe, ProcessRecipe, CookingRecipe, WeigthRecipe

class RecipeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Titre'

    class Meta :
        model = Recipe
        fields = '__all__' 
        exclude = ('author',)


    def clean_servings(self):
        value = self.cleaned_data.get("servings")
        print(value)
        if value < 1:
            raise forms.ValidationError("The number of servings must be greater than zero.")
        return value
        
class IngredientForm(forms.ModelForm):

    class Meta:
        model = IngredientRecipe
        exclude = ('recipe',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['forme'].label = 'ingredient'
        self.fields['name'].label = 'forme'

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.fields['ingredient'].queryset = Ingredient.objects.all().order_by('name')
        self.fields['ingredient'].queryset = Ingredient.objects.all()
        self.fields['famille'].queryset = Famille.objects.all()
        self.fields['forme'].queryset = Forme.objects.all()

        #print(self.data)
        
        #if 'ingredient' in self.data:
        #    try:
        #        famille_id1 = int(self.data.get('famille'))
        #        self.fields['ingredient'].queryset = Ingredient.objects.filter(pk =famille_id1).order_by('name')
        #    except (ValueError, TypeError):
        #        pass  # invalid input from the client; ignore and fallback to empty City queryset
        #elif self.instance.pk:
        #    self.fields['ingredient'].queryset = self.instance.famille.famille_ingredient.order_by('name')

IngredientFormSet = forms.inlineformset_factory(Recipe, IngredientRecipe, form=IngredientForm, extra=0)

class ProcessForm(forms.ModelForm):
    step = forms.CharField(widget=forms.Textarea)
    #short_desc = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = ProcessRecipe
        exclude = ('recipe',)

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['step'].widget.attrs['style'] = 'width:80%; height:40px;'
        #self.fields['long_desc'].widget.attrs['style']  = 'width:800px; height:80px;'

class CookingForm(forms.ModelForm):
    step = forms.CharField(widget=forms.Textarea)
    #short_desc = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = CookingRecipe
        exclude = ('recipe',)

    def __init__(self, *args, **kwargs):
        super(CookingForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['step'].widget.attrs['style'] = 'width:80%; height:40px;'
        #self.fields['long_desc'].widget.attrs['style']  = 'width:800px; height:80px;'



class WeigthForm(forms.ModelForm):
    class Meta:
        model = WeigthRecipe
        exclude = ('recipe',)

    #def __init__(self, *args, **kwargs):
    #    super(CookingForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
    #    self.fields['step'].widget.attrs['style'] = 'width:80%; height:40px;'
        #self.fields['long_desc'].widget.attrs['style']  = 'width:800px; height:80px;'




ProcessFormSet = forms.inlineformset_factory(Recipe, ProcessRecipe, form=ProcessForm, extra=0)
CookingFormSet = forms.inlineformset_factory(Recipe, CookingRecipe, form=CookingForm, extra=0)
WeightFormSet = forms.inlineformset_factory(Recipe, WeigthRecipe, form=WeigthForm, extra=0)



Formset_Params = {
    'form-TOTAL_FORMS' : '100',
    'form-INITIAL_FORMS' : '1',
    'form-MIN_NUM_FORMS' : '1', 
}    
