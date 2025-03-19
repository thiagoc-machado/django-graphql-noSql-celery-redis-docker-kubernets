from django.test import TestCase
from .models import Produto

class ProdutoTest(TestCase):
    def test_criar_produto(self):
        produto = Produto.objects.create(nome='Teste', preco=10.0, dados_extras={'cor': 'azul'})
        self.assertEqual(produto.dados_extras['cor'], 'azul')
