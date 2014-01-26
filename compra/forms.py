from clubeoferta.compra.models import cadastro_pagseguro

class form_cadastro_pagseguro(forms.ModelForm):
    class Meta:
        model = cadastro_pagseguro()
