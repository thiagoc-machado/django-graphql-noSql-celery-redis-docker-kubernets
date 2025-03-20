import graphene
from graphene_django.types import DjangoObjectType
from graphene.types.generic import GenericScalar  # Use GenericScalar to accept any JSON object
from .models import Usuario, Telefone, CategoriaTelefone, TipoTelefone
from django.core.cache import cache

class TelefoneType(DjangoObjectType):
    metadata = GenericScalar()

    class Meta:
        model = Telefone
        fields = ("id", "numero", "metadata", "categoria", "tipo")

class UsuarioType(DjangoObjectType):
    detalhes = GenericScalar()
    telefones = graphene.List(TelefoneType)

    class Meta:
        model = Usuario
        fields = ("id", "nome", "detalhes")

    def resolve_telefones(self, info):
        return self.telefones.all()

class CategoriaTelefoneType(DjangoObjectType):
    class Meta:
        model = CategoriaTelefone
        fields = ("id", "nome")

class TipoTelefoneType(DjangoObjectType):
    class Meta:
        model = TipoTelefone
        fields = ("id", "nome", "categoria")

class Query(graphene.ObjectType):
    usuarios = graphene.List(UsuarioType)
    telefones = graphene.List(TelefoneType)
    categorias_telefone = graphene.List(CategoriaTelefoneType)

    def resolve_usuarios(self, info):
        cached_data = cache.get('usuarios')
        if cached_data:
            return cached_data
        usuarios = Usuario.objects.all()
        cache.set('usuarios', usuarios, timeout=60)
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
        detalhes = GenericScalar()
        telefones = graphene.List(GenericScalar)

    usuario = graphene.Field(UsuarioType)

    def mutate(self, info, nome, detalhes=None, telefones=None):
        usuario = Usuario(nome=nome, detalhes=detalhes or {})
        usuario.save()
        if telefones:
            for tel in telefones:
                categoria_name = tel.get('categoria')
                tipo_name = tel.get('tipo')
                # Get or create the category
                categoria_instance = None
                if categoria_name:
                    categoria_instance, _ = CategoriaTelefone.objects.get_or_create(nome=categoria_name)
                
                # Get or create the type linked to the category, if available
                tipo_instance = None
                if tipo_name and categoria_instance:
                    tipo_instance, _ = TipoTelefone.objects.get_or_create(
                        nome=tipo_name,
                        categoria=categoria_instance
                    )
                Telefone.objects.create(
                    usuario=usuario,
                    numero=tel.get('numero'),
                    categoria=categoria_instance,
                    tipo=tipo_instance,
                    metadata=tel.get('metadata', {})
                )
        cache.delete('usuarios')
        return CriarUsuario(usuario=usuario)

class AtualizarUsuario(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        nome = graphene.String(required=True)
        detalhes = GenericScalar()
        telefones = graphene.List(GenericScalar)

    usuario = graphene.Field(UsuarioType)

    def mutate(self, info, id, nome, detalhes=None, telefones=None):
        usuario = Usuario.objects.get(pk=id)
        usuario.nome = nome
        if detalhes is not None:
            usuario.detalhes = detalhes
        usuario.save()
        if telefones:
            # Here you might update existing phone records or create new ones.
            for tel in telefones:
                categoria_name = tel.get('categoria')
                tipo_name = tel.get('tipo')
                categoria_instance = None
                tipo_instance = None
                if categoria_name:
                    try:
                        categoria_instance = CategoriaTelefone.objects.get(nome=categoria_name)
                    except CategoriaTelefone.DoesNotExist:
                        pass
                if tipo_name:
                    try:
                        tipo_instance = TipoTelefone.objects.get(nome=tipo_name)
                    except TipoTelefone.DoesNotExist:
                        pass
                Telefone.objects.create(
                    usuario=usuario,
                    numero=tel.get('numero'),
                    categoria=categoria_instance,
                    tipo=tipo_instance,
                    metadata=tel.get('metadata', {})
                )
        cache.delete('usuarios')
        return AtualizarUsuario(usuario=usuario)

class DeletarUsuario(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        usuario = Usuario.objects.get(pk=id)
        usuario.delete()
        cache.delete('usuarios')
        return DeletarUsuario(success=True)

class Mutacao(graphene.ObjectType):
    criar_usuario = CriarUsuario.Field()
    atualizar_usuario = AtualizarUsuario.Field()
    deletar_usuario = DeletarUsuario.Field()

schema = graphene.Schema(query=Query, mutation=Mutacao)
