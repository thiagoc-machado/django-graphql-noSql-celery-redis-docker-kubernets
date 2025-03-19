import graphene
from graphene_django.types import DjangoObjectType
from .models import Usuario, Telefone, CategoriaTelefone, TipoTelefone
from django.core.cache import cache

class UsuarioType(DjangoObjectType):
    class Meta:
        model = Usuario

class TelefoneType(DjangoObjectType):
    class Meta:
        model = Telefone

class CategoriaTelefoneType(DjangoObjectType):
    class Meta:
        model = CategoriaTelefone

class TipoTelefoneType(DjangoObjectType):
    class Meta:
        model = TipoTelefone

class Query(graphene.ObjectType):
    usuarios = graphene.List(UsuarioType)
    telefones = graphene.List(TelefoneType)
    categorias_telefone = graphene.List(CategoriaTelefoneType)

    def resolve_usuarios(self, info):
        cached_data = cache.get('usuarios')
        if cached_data:
            return cached_data

        usuarios = Usuario.objects.all()
        cache.set('usuarios', usuarios, timeout=60)  # Cache por 60s
        return usuarios

    def resolve_telefones(self, info):
        cached_data = cache.get('telefones')
        if cached_data:
            return cached_data

        telefones = Telefone.objects.all()
        cache.set('telefones', telefones, timeout=60)
        return telefones

    def resolve_categorias_telefone(self, info):
        cached_data = cache.get('categorias_telefone')
        if cached_data:
            return cached_data

        categorias = CategoriaTelefone.objects.all()
        cache.set('categorias_telefone', categorias, timeout=60)
        return categorias
    
class CriarUsuario(graphene.Mutation):
    class Arguments:
        nome = graphene.String(required=True)

    usuario = graphene.Field(UsuarioType)

    def mutate(self, info, nome):
        usuario = Usuario(nome=nome)
        usuario.save()
        cache.delete('usuarios')  # Invalida o cache ao criar
        return CriarUsuario(usuario=usuario)

class AtualizarUsuario(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        nome = graphene.String(required=True)

    usuario = graphene.Field(UsuarioType)

    def mutate(self, info, id, nome):
        usuario = Usuario.objects.get(pk=id)
        usuario.nome = nome
        usuario.save()
        cache.delete('usuarios')  # Invalida o cache ao atualizar
        return AtualizarUsuario(usuario=usuario)

class DeletarUsuario(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        usuario = Usuario.objects.get(pk=id)
        usuario.delete()
        cache.delete('usuarios')  # Invalida o cache ao deletar
        return DeletarUsuario(success=True)

class Mutacao(graphene.ObjectType):
    criar_usuario = CriarUsuario.Field()
    atualizar_usuario = AtualizarUsuario.Field()
    deletar_usuario = DeletarUsuario.Field()

schema = graphene.Schema(query=Query, mutation=Mutacao)

