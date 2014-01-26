ClubeOferta
===========

Antigo Projeto de  Site de Compra Coletiva feito sobre o Django 1.2, o projeto inicial era chamado de Clube Oferta, mas foi lançado posteriormente como Pegada Coletiva. Foi meu segundo projeto em Django, haverá bastante espaço para arrumação.
Este site contem cadastro de anuncios de compra coletiva e integração com Pagseguro, recebe também os dados automaticamente sobre o pagamento.


Requisitos
=======
django==1.2<br>
pillow

Instalação
===
Verifique se você possui os requisitos, caso não possua, instale os requisitos com pip:
    `pip install -r requirements.txt`
    
Crie a base de dados e cadastre um superuser do sistema.: 
    `python manage.py syncdb`

Preencha as configurações de e-mail que estão no settings.py
      ```
      
      #Configurações de E-mail
      
      EMAIL_HOST = ''
      EMAIL_HOST_USER = ''
      EMAIL_HOST_PASSWORD = ''
      EMAIL_SUBJECT_PREFIX = ''
      EMAIL_PORT = 587
      EMAIL_USE_TLS=True
      SERVER_EMAIL = ""
      
Coloque o Email responsável pela sua conta no pagseguro: `E_MAIL_COBRANCA = ""` e o `TOKEN = ""` gerado lá. Também defina a URL de Retorno do Pagseguro para o www.enderecodasualoja.com.br/retorno/pagseguro/



Em seguida rode o servidor de desenvolvimento: 
    `python manage.py runserver`

Acesse o endereço do admin e faça o login com seu super-usuário:
    `http://localhost:8000/admin`
    

Crie um Anúncio preenchendo todos os campos obrigatórios

Ainda no Admin (`http://localhost:8000/admin`) crie as páginas planas que o site possui com as seguintes urls:

como-funciona<br>
faq<br>
sobre<br>
imprensa<br>
politica<br>
termos<br>
trabalhe-conosco


No final da oferta execute uma tarefa no cron para gerar os vouchers e enviar um email aos compradores `python manage.py vouchers`
