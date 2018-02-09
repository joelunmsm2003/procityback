from django.contrib import admin
from app.models import *
from django.contrib.admin import RelatedOnlyFieldListFilter

from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from PIL import Image
from resizeimage import resizeimage
import os.path
from PIL import Image
from resizeimage import resizeimage

from django.contrib import admin

# Register your models here.



def resize_and_crop(img_path, modified_path, size, crop_type='top'):
	"""
	Resize and crop an image to fit the specified size.
	args:
		img_path: path for the image to resize.
		modified_path: path to store the modified image.
		size: `(width, height)` tuple.
		crop_type: can be 'top', 'middle' or 'bottom', depending on this
			value, the image will cropped getting the 'top/left', 'midle' or
			'bottom/rigth' of the image to fit the size.
	raises:
		Exception: if can not open the file in img_path of there is problems
			to save the image.
		ValueError: if an invalid `crop_type` is provided.
	"""
	# If height is higher we resize vertically, if not we resize horizontally
	img = Image.open(img_path)
	# Get current and desired ratio for the images
	img_ratio = img.size[0] / float(img.size[1])
	ratio = size[0] / float(size[1])
	#The image is scaled/cropped vertically or horizontally depending on the ratio
	if ratio > img_ratio:
		img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
				Image.ANTIALIAS)
		# Crop in the top, middle or bottom
		if crop_type == 'top':
			box = (0, 0, img.size[0], size[1])
		elif crop_type == 'middle':
			box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
		elif crop_type == 'bottom':
			box = (0, img.size[1] - size[1], img.size[0], img.size[1])
		else :
			raise ValueError('ERROR: invalid value for crop_type')
		img = img.crop(box)
	elif ratio < img_ratio:
		img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
				Image.ANTIALIAS)
		# Crop in the top, middle or bottom
		if crop_type == 'top':
			box = (0, 0, size[0], img.size[1])
		elif crop_type == 'middle':
			box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
		elif crop_type == 'bottom':
			box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
		else :
			raise ValueError('ERROR: invalid value for crop_type')
		img = img.crop(box)
	else :
		img = img.resize((size[0], size[1]),
				Image.ANTIALIAS)
		# If the scale is the same, we do not need to crop
	img.save(modified_path)

@admin.register(Smsrecibidos)
class SmsrecibidosAdmin(admin.ModelAdmin):
	list_display = ('text','when','sender','receiver')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','orden')
	list_editable = ('orden',)

	def save_model(self, request, obj, form, change):
		
		super(CategoriaAdmin, self).save_model(request, obj, form, change)
		
		if Categoria.objects.get(id=obj.id).photo:

			caption = '/home/backmylook/'+str(Categoria.objects.get(id=obj.id).photo)

			resize_and_crop(caption, caption, (828,315), crop_type='top')


@admin.register(Subcategoria)
class SubCategoriaAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','categoria','orden')
	list_editable = ('nombre','orden')
	list_filter = ('categoria__nombre',)

	def categoria(self, obj):
		return obj.nombre


	def save_model(self, request, obj, form, change):
			
		super(SubCategoriaAdmin, self).save_model(request, obj, form, change)
		
		if Subcategoria.objects.get(id=obj.id).photo:

			caption = '/home/backmylook/'+str(Subcategoria.objects.get(id=obj.id).photo)

			resize_and_crop(caption, caption, (500,150), crop_type='top')

@admin.register(Tiponotificacion)
class TiponotificacionAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','plantilla')
	list_editable = ('nombre',)


@admin.register(Portadaphoto)
class PortadaphotoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre')
	list_editable = ('nombre',)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre')
	list_editable = ('nombre',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	list_display = ('id','user')
	search_fields = ('user__email','user__username')

	def user(self, obj):
		return obj.user.username



@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre')
	list_editable = ('nombre',)


@admin.register(Dia)
class DiaAdmin(admin.ModelAdmin):
	list_display = ('id','nombre')

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
	list_display = ('id','fecha','tipo','cliente','descripcion')

	def tipo(self, obj):
		return obj.tipo_notificacion.nombre


	def cliente(self, obj):
		return obj.cliente.nombre




@admin.register(Estadosocia)
class EstadosociaAdmin(admin.ModelAdmin):
	list_display = ('id','nombre')
	list_editable = ('nombre',)


# @admin.register(Distrito)
# class DistritoAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre')
# 	list_editable = ('nombre',)

@admin.register(Socia)
class SociaAdmin(admin.ModelAdmin):
	list_display = ('id','user','nombre','apellido','dni','telefono','direccion','distrito','referencia','texperiencia','estado_socia')
	list_filter= ('estado_socia',)


@admin.register(Sociasubcategoria)
class SociasubcategoriaAdmin(admin.ModelAdmin):
	list_display = ('id','socia','subcategoria')
	list_filter=('socia__nombre',)

	
	def socia(self, obj):
		return obj.socia.nombre

	def subcategoria(self, obj):
		return obj.subcategoria.nombre

# @admin.register(Opcion)
# class OpcionAdmin(admin.ModelAdmin):
# 	list_display = ('id','sociasubcategoria','nombre')

	
# 	def sociasubcategoria(self, obj):
# 		return str(obj.sociasubcategoria.socia.nombre)+str(obj.sociasubcategoria.subcategoria.nombre)

@admin.register(Turnosocia)
class TurnosociaAdmin(admin.ModelAdmin):
	list_display = ('id','socia','fecha_inicio','fecha_fin','dia')
	list_filter=('socia__nombre','dia')

	

	def socia(self, obj):
		return obj.socia.nombre


@admin.register(Clientesocias)
class ClientessociasAdmin(admin.ModelAdmin):
	list_display = ('id','cliente','socia')

	
	def cliente(self, obj):
		return obj.cliente.nombre

	def socia(self, obj):
		return obj.socia.nombre


@admin.register(Sociadistrito)
class SociadistritoAdmin(admin.ModelAdmin):
	list_display = ('socia','distrito')


	
	def socia(self, obj):
		return obj.socia.nombre

	def distrito(self, obj):
		return obj.distrito.nombre



@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
	list_display = ('id','get_cliente','socia','estado')
	list_filter = ('estado__nombre',)
	# actions=['enviar_notificacion']

	# def enviar_notificacion(self, request, queryset):

	# 	for obj in queryset:

	# 		print obj.cliente.nombre

	# return None

	def get_cliente(self, obj):
		return obj.cliente.user.first_name
	def socia(self, obj):
		return obj.socia.nombre

	



@admin.register(Serviciopedido)
class ServiciopedidoAdmin(admin.ModelAdmin):
	list_display = ('servicio','socia','cliente','categoria','subcategoria','estado','fecha','hora')
	list_filter=('servicio__estado','servicio')
	
	def categoria(self, obj):
		return obj.subcategoria.categoria.nombre

	def sociasubcategoria(self, obj):
		return obj.subcategoria.nombre


	def cliente(self, obj):
		return obj.servicio.cliente.user.first_name


	def socia(self, obj):
		return obj.servicio.socia.nombre

	def estado(self, obj):
		return obj.servicio.estado.nombre

	def fecha(self, obj):
		return obj.servicio.fecha

	def hora(self, obj):
		return obj.servicio.fecha_inicio



# @admin.register(Pais)
# class PaisAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(EstadoCivil)
# class EstadoCivilAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Modalidad)
# class ModalidadAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Nivel)
# class NivelAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre','descripcion')
#     list_editable = ('nombre',)

# @admin.register(TipoAgente)
# class TipoAgenteAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Grupo)
# class GrupoAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Subgrupo)
# class SubgrupoAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Compania)
# class CompaniaAgenteAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Producto)
# class ProductoAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Ramo)
# class RamoAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(TipoCita)
# class TipoCitaAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(TipoSeguimiento)
# class TipoSeguimientoAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Relacion)
# class RelacionAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Equipo)
# class EquipoAdmin(admin.ModelAdmin):
#     list_display = ('id','nombre')
#     list_editable = ('nombre',)

# @admin.register(Semanas)
# class SemanasAdmin(admin.ModelAdmin):
#     list_display = ('id','numero','fecha_inicio','fecha_fin','anio')



# @admin.register(Agente)
# class AgenteAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_estructura','get_user','get_tipo_agente','meta_personal','meta_requerida','fecha_ingreso','correo_capital','photo')
# 	list_editable = ('meta_personal',)


# 	def save_model(self, request, obj, form, change):
		
# 		super(AgenteAdmin, self).save_model(request, obj, form, change)
		

# 		# caption = '/home/capital_back/'+str(Agente.objects.get(id=obj.id).photo)
# 		# fd_img = open(caption, 'r')
# 		# img = Image.open(fd_img)
# 		# width, height = img.size
# 		# img = resizeimage.resize_cover(img, [300, 300])
# 		# img.save(caption, img.format)
# 		# fd_img.close()
	
# 	def get_user(self, obj):

# 		if obj.user:
# 			return obj.user.username
# 		else:
# 			return ''

# 	def get_tipo_agente(self, obj):

# 		if obj.tipo_agente:
# 			return obj.tipo_agente.nombre
# 		else:
# 			return ''
# 	def get_estructura(self, obj):
		
# 		if obj.estructura:
# 			return obj.estructura.nombre
# 		else:
# 			return ''


# @admin.register(Cliente)
# class ClienteAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_user','fecha_inicio','estado_civil','numero_hijos')
# 	list_editable = ('estado_civil',)

# 	def get_user(self, obj):
# 		return obj.user.username

# @admin.register(Citas)
# class CitasAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_cliente','get_agente','get_tipo_cita','get_propuesta_cliente','get_tipo_seguimiento','fecha_cita','fecha_creacion','prima_target','inforce')
# 	list_filter = ('tipo_seguimiento__nombre','tipo_cita__nombre','agente__user__username')
# 	list_editable = ('inforce',)

# 	def get_agente(self, obj):
# 		return obj.agente.user.first_name

# 	def get_tipo_cita(self, obj):
# 		return obj.tipo_cita.nombre

# 	def get_cliente(self, obj):
# 		return obj.cliente.user.first_name


# 	def get_propuesta_cliente(self, obj):
# 		return obj.propuesta_cliente.ramo_compania_producto.ramo.nombre

# 	def get_tipo_seguimiento(self, obj):
# 		return obj.tipo_seguimiento.nombre




# @admin.register(ParientesCliente)
# class ParientesClienteAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_cliente','nombre','edad','relacion')
	

# 	def get_cliente(self, obj):
# 		return obj.cliente.user.username


# @admin.register(PropuestaCliente)
# class PropuestaClienteAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_cliente','get_agente','get_ramo','observacion','fecha','detalle','inforce')
# 	list_editable = ('inforce',)
	
# 	def get_cliente(self, obj):
# 		return obj.cliente.user.username

# 	def get_agente(self, obj):
# 		return obj.agente.user.username

# 	def get_ramo(self, obj):
# 		return obj.ramo_compania_producto.ramo.nombre + ' / ' + obj.ramo_compania_producto.compania.nombre +' / '+obj.ramo_compania_producto.producto.nombre

# @admin.register(RamoCompaniaProducto)
# class RamoCompaniaProductoAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_ramo','get_compania','get_producto')
	
# 	def get_ramo(self, obj):
# 		return obj.ramo.nombre

# 	def get_compania(self, obj):
# 		return obj.compania.nombre

# 	def get_producto(self, obj):
# 		return obj.producto.nombre


# # class DatosInline(admin.StackedInline):
# #     model = DatosUsuario
# #     can_delete = False


# # # Define a new User admin
# # class UserAdmin(BaseUserAdmin):
# #     inlines = (DatosInline, )

# # # Re-register UserAdmin
# # admin.site.unregister(User)
# # admin.site.register(User, UserAdmin)



# @admin.register(TelefonoUser)
# class TelefonoUserAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_user','numero')
	
# 	def get_user(self, obj):
# 		return obj.user.username


# @admin.register(Iconos)
# class IconosAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre','icono')
	



# @admin.register(AuthUser)
# class AuthUserAdmin(admin.ModelAdmin):
# 	list_display = ('id','pais','get_equipo','username','first_name','last_name','get_nivel','get_grupo','get_subgrupo','correo_capital','email','nacimiento','telefono','direccion','dni','contacto','relacion','movil_contacto','fecha_ingreso')
# 	#list_editable = ('email',)
# 	search_fields = ('first_name',)
# 	list_filter = ('nivel__nombre','equipo__nombre')





# 	def save_model(self, request, obj, form, change):



# 		if Agente.objects.filter(user_id=obj.id):

# 			age_obj = Agente.objects.get(user_id=obj.id)
# 			age_obj.equipo=obj.equipo
# 			age_obj.tipo_agente_id=obj.tipo_agente
# 			age_obj.meta_personal=obj.meta_personal
# 			age_obj.meta_requerida=obj.meta_requerida
# 			age_obj.fecha_ingreso=obj.fecha_ingreso
# 			age_obj.correo_capital=obj.correo_capital
# 			age_obj.photo=obj.photo
# 			age_obj.save()

# 		else:

# 			print 'nivel',obj.nivel

# 			if obj.nivel:

# 				if obj.nivel.nombre!='Cliente':


# 					if obj.tipo_agente:

# 						id_tipo_agente = obj.tipo_agente.id

# 					else:

# 						id_tipo_agente = None


# 					Agente(photo=obj.photo,user_id=obj.id,tipo_agente_id=id_tipo_agente,meta_requerida=obj.meta_requerida,meta_personal=obj.meta_requerida,fecha_ingreso=obj.fecha_ingreso,correo_capital=obj.correo_capital,equipo=obj.equipo).save()

# 		super(AuthUserAdmin, self).save_model(request, obj, form, change)

# 		caption = '/home/capital_back/'+str(AuthUser.objects.get(id=obj.id).photo)

# 		if os.path.isfile(caption):
		
# 			fd_img = open(caption, 'r')
# 			img = Image.open(fd_img)
# 			width, height = img.size
# 			img = resizeimage.resize_cover(img, [300, 300])
# 			img.save(caption, img.format)
# 			fd_img.close()


# 	def get_nivel(self, obj):

# 		if obj.nivel:
# 				return obj.nivel.nombre
# 		else:
# 				return ''
# 	get_nivel.short_description = 'Nivel'
# 	get_nivel.admin_order_field = 'equipo_id'

# 	def get_grupo(self, obj):

# 		if obj.grupo:
# 				return obj.grupo.nombre
# 		else:
# 				return ''
# 	get_grupo.short_description = 'Grupo'
# 	get_grupo.admin_order_field = 'equipo_id'

# 	def get_subgrupo(self, obj):

# 		if obj.subgrupo:
# 				return obj.subgrupo.nombre
# 		else:
# 				return ''
# 	get_subgrupo.short_description = 'Subgrupo'
# 	get_subgrupo.admin_order_field = 'equipo_id'


# 	def get_equipo(self, obj):

# 		if obj.equipo:
# 				return obj.equipo.nombre
# 		else:
# 				return ''

# 	get_equipo.short_description = 'Equipo'
# 	get_equipo.admin_order_field = 'equipo_id'



