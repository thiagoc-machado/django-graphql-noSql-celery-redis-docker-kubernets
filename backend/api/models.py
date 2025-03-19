from django.db import models

class Usuario(models.Model):
    nome = models.CharField(max_length=255)

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

    def __str__(self):
        return f'{self.numero} - {self.usuario.nome}'
