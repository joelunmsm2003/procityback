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

# @admin.register(Smsrecibidos)
# class SmsrecibidosAdmin(admin.ModelAdmin):
# 	list_display = ('text','when','sender','receiver')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','orden')
	list_editable = ('orden',)

	def save_model(self, request, obj, form, change):
		
		super(CategoriaAdmin, self).save_model(request, obj, form, change)
		
		if Categoria.objects.get(id=obj.id).photo:

			caption = '/home/procity/'+str(Categoria.objects.get(id=obj.id).photo)

			resize_and_crop(caption, caption, (828,315), crop_type='top')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','orden')
	list_editable = ('orden',)

	def save_model(self, request, obj, form, change):
		
		super(MenuAdmin, self).save_model(request, obj, form, change)
		
		if Menu.objects.get(id=obj.id).photo:

			caption = '/home/procity/'+str(Menu.objects.get(id=obj.id).photo)

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

			caption = '/home/procity/'+str(Subcategoria.objects.get(id=obj.id).photo)

			resize_and_crop(caption, caption, (500,150), crop_type='top')

# @admin.register(Tiponotificacion)
# class TiponotificacionAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre','plantilla')
# 	list_editable = ('nombre',)


@admin.register(Portadaphoto)
class PortadaphotoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre')
	list_editable = ('nombre',)

# @admin.register(Estado)
# class EstadoAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre')
# 	list_editable = ('nombre',)

# @admin.register(Cliente)
# class ClienteAdmin(admin.ModelAdmin):
# 	list_display = ('id','user')
# 	search_fields = ('user__email','user__username')

# 	def user(self, obj):
# 		return obj.user.username



# @admin.register(Distrito)
# class DistritoAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre')
# 	list_editable = ('nombre',)


# @admin.register(Dia)
# class DiaAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre')

# @admin.register(Notificacion)
# class NotificacionAdmin(admin.ModelAdmin):
# 	list_display = ('id','fecha','tipo','cliente','descripcion')

# 	def tipo(self, obj):
# 		return obj.tipo_notificacion.nombre


# 	def cliente(self, obj):
# 		return obj.cliente.nombre




# @admin.register(Estadosocia)
# class EstadosociaAdmin(admin.ModelAdmin):
# 	list_display = ('id','nombre')
# 	list_editable = ('nombre',)


# # @admin.register(Distrito)
# # class DistritoAdmin(admin.ModelAdmin):
# # 	list_display = ('id','nombre')
# # 	list_editable = ('nombre',)

# @admin.register(Socia)
# class SociaAdmin(admin.ModelAdmin):
# 	list_display = ('id','user','nombre','apellido','dni','telefono','direccion','distrito','referencia','texperiencia','estado_socia')
# 	list_filter= ('estado_socia',)


# @admin.register(Sociasubcategoria)
# class SociasubcategoriaAdmin(admin.ModelAdmin):
# 	list_display = ('id','socia','subcategoria')
# 	list_filter=('socia__nombre',)

	
# 	def socia(self, obj):
# 		return obj.socia.nombre

# 	def subcategoria(self, obj):
# 		return obj.subcategoria.nombre

# # @admin.register(Opcion)
# # class OpcionAdmin(admin.ModelAdmin):
# # 	list_display = ('id','sociasubcategoria','nombre')

	
# # 	def sociasubcategoria(self, obj):
# # 		return str(obj.sociasubcategoria.socia.nombre)+str(obj.sociasubcategoria.subcategoria.nombre)

# @admin.register(Turnosocia)
# class TurnosociaAdmin(admin.ModelAdmin):
# 	list_display = ('id','socia','fecha_inicio','fecha_fin','dia')
# 	list_filter=('socia__nombre','dia')

	

# 	def socia(self, obj):
# 		return obj.socia.nombre


# @admin.register(Clientesocias)
# class ClientessociasAdmin(admin.ModelAdmin):
# 	list_display = ('id','cliente','socia')

	
# 	def cliente(self, obj):
# 		return obj.cliente.nombre

# 	def socia(self, obj):
# 		return obj.socia.nombre


# @admin.register(Sociadistrito)
# class SociadistritoAdmin(admin.ModelAdmin):
# 	list_display = ('socia','distrito')


	
# 	def socia(self, obj):
# 		return obj.socia.nombre

# 	def distrito(self, obj):
# 		return obj.distrito.nombre



# @admin.register(Servicio)
# class ServicioAdmin(admin.ModelAdmin):
# 	list_display = ('id','get_cliente','socia','estado')
# 	list_filter = ('estado__nombre',)
# 	# actions=['enviar_notificacion']

# 	# def enviar_notificacion(self, request, queryset):

# 	# 	for obj in queryset:

# 	# 		print obj.cliente.nombre

# 	# return None

# 	def get_cliente(self, obj):
# 		return obj.cliente.user.first_name
# 	def socia(self, obj):
# 		return obj.socia.nombre

	



# @admin.register(Serviciopedido)
# class ServiciopedidoAdmin(admin.ModelAdmin):
# 	list_display = ('servicio','socia','cliente','categoria','subcategoria','estado','fecha','hora')
# 	list_filter=('servicio__estado','servicio')
	
# 	def categoria(self, obj):
# 		return obj.subcategoria.categoria.nombre

# 	def sociasubcategoria(self, obj):
# 		return obj.subcategoria.nombre


# 	def cliente(self, obj):
# 		return obj.servicio.cliente.user.first_name


# 	def socia(self, obj):
# 		return obj.servicio.socia.nombre

# 	def estado(self, obj):
# 		return obj.servicio.estado.nombre

# 	def fecha(self, obj):
# 		return obj.servicio.fecha

# 	def hora(self, obj):
# 		return obj.servicio.fecha_inicio


