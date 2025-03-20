from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    detalhes = models.JSONField(default=dict, blank=True, null=True)
    # The 'detalhes' field can store nested data like address, preferences, social links, etc.

    def __str__(self):
        return self.nome

class CategoriaTelefone(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class TipoTelefone(models.Model):
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey(CategoriaTelefone, on_delete=models.CASCADE, related_name='tipos')

    def __str__(self):
        return self.nome

class Telefone(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='telefones')
    numero = models.CharField(max_length=20)
    categoria = models.ForeignKey(CategoriaTelefone, on_delete=models.SET_NULL, null=True)
    tipo = models.ForeignKey(TipoTelefone, on_delete=models.SET_NULL, null=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    # The 'metadata' field can hold additional, nested information about the phone, 
    # such as verification, history, provider details, location, etc.

    def __str__(self):
        return f'{self.numero} - {self.usuario.nome}'
