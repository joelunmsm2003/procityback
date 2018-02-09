#    ___       ___       ___       ___            ___       ___   
#   /\  \     /\__\     /\  \     /\__\          /\  \     /\  \  
#  /  \  \   / | _|_   /  \  \   |  L__L        _\ \  \   /  \  \ 
# /  \ \__\ /  |/\__\ / /\ \__\  |   \__\      /\/  \__\ / /\ \__\
# \/\  /  / \/|  /  / \ \/ /  /  /   /__/      \  /\/__/ \ \/ /  /
#   / /  /    | /  /   \  /  /   \/__/          \/__/     \  /  / 
#   \/__/     \/__/     \/__/                              \/__/

# email : joelunmsm@gmail.com
# web   : xiencias.com



from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth import *
from django.views.generic import View
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import Group, User
from jwt_auth.compat import json
from jwt_auth.mixins import JSONWebTokenAuthMixin
from django.template import RequestContext
import simplejson
from django.views.decorators.csrf import csrf_exempt
import xlrd
from django.db.models import Count,Sum
from app.models import *
from app.serializers import *

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

from django.contrib.auth import authenticate
import time
from django.db.models import Func
import os
from datetime import datetime,timedelta,date
import os.path
import requests
import smtplib
from email.mime.text import MIMEText
from django.db.models import Count,Max
import datetime
import random
from django.db.models import Count,Sum
from PIL import Image
from resizeimage import resizeimage
from django.core.mail import EmailMultiAlternatives

import operator
from django.db.models import Q

import datetime
import requests
import json

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



@csrf_exempt
def prueba(request):


	c= Categoria.objects.all().values('id','nombre','photo')

	c= simplejson.dumps(ValuesQuerySetToDict(c))

	return HttpResponse(c, content_type="application/json")

@csrf_exempt
def registro(request):


	username= json.loads(request.body)['email']

	password= json.loads(request.body)['password']


	if User.objects.filter(username=username).count()>0:

		c= simplejson.dumps(0)

		return HttpResponse(c, content_type="application/json")



	User.objects.create_user(username, username, password)

	id_user = User.objects.all().values('id').order_by('-id')[0]['id']

	u = User.objects.get(id=id_user)
	u.first_name= json.loads(request.body)['nombre']

	u.save()


	group = Group.objects.get(name='Cliente')
	u.groups.add(group)




	Cliente(user_id=id_user,email=username).save()
	
	user = authenticate(username=username, password=password)
	login(request, user)


	#Agrega el ID Device


	archivo = open("/home/dd.txt", 'r') 
	i=0
	for linea in archivo.readlines():
		i=i+1
		if int(i)==22:     
			t=linea


	player = json.loads(t)['players']


	for p in player:



		header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic OGQyNTllMmUtMmY2Ny00ZGQxLWEzNWMtMjM5NTdlNjM0ZTc3"}
		payload = {"app_id": "6d06ccb5-60c3-4a76-83d5-9363fbf6b40a","include_player_ids": [p['id']],"contents": {"en": "Bienvenida a My Look Xpress"},"data":{'codigo': p['id']}}
		req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
		print(req.status_code, req.reason)


	c= simplejson.dumps('ok')

	return HttpResponse(c, content_type="application/json")

@csrf_exempt
def smsrecibidos(request):


    f = open('/var/www/codigito.com/public_html/recibidos.txt', 'a')
    f.write(str(request.GET)+'\n')
    f.close()
    text = request.GET['text']
    when = request.GET['when']
    sender = request.GET['sender']
    receiver = request.GET['receiver']
    Smsrecibidos(text=text,when=when,sender=sender,receiver=receiver).save()

    return HttpResponse('OK', content_type="application/json")



@csrf_exempt
def carganoti(request,perfil,id_cliente):


	archivo = open("/home/dd.txt", 'r') 
	i=0
	for linea in archivo.readlines():
		i=i+1
		if int(i)==22:     
			t=linea


	player = json.loads(t)['players']


	for p in player:

		header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic OGQyNTllMmUtMmY2Ny00ZGQxLWEzNWMtMjM5NTdlNjM0ZTc3"}
		payload = {"app_id": "6d06ccb5-60c3-4a76-83d5-9363fbf6b40a","include_player_ids": [p['id']],"contents": {"en": "Bienvenida a My Look Xpress"},"data":{'codigo': p['id']}}
		req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
		print(req.status_code, req.reason)

	a= simplejson.dumps('OK')
		
	return HttpResponse(a, content_type="application/json")

class Uploadphoto(JSONWebTokenAuthMixin, View):

	#Retorna datos del agente
	def post(self, request):

		caption = request.FILES['file']

		#Guarda foto

		print caption

		id_user =request.user.id

		print id_user

		a = Agente.objects.get(user_id=id_user)

		a.photo = caption
		a.save()


		caption = '/home/capital_back/'+str(Agente.objects.get(user_id=id_user).photo)

		fd_img = open(caption, 'r')

		img = Image.open(fd_img)

		width, height = img.size

		img = resizeimage.resize_cover(img, [300, 300])

		img.save(caption, img.format)

		fd_img.close()

		a= simplejson.dumps('OK')
		
		return HttpResponse(a, content_type="application/json")




def mobile(request):
	"""Return True if the request comes from a mobile device."""
	MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
	if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
		return True
	else:
		return False

def ValuesQuerySetToDict(vqs):

	return [item for item in vqs]


## Agrega telefonos
def envianotificacion(request,tipo):

	if tipo=='Compartir':



		plantilla = Tiponotificacion.objects.get(nombre=tipo).plantilla
		
		c= simplejson.dumps(plantilla)

		print 'entre a compartir'

		return HttpResponse(c, content_type="application/json")

	else:


		return HttpResponse(simplejson.dumps('u'), content_type="application/json")


class Sacauser(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self, request):

		id=request.user.id

		c=User.objects.filter(id=id).values('id','username','groups__name')
		
		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")


class Sacasocia(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self, request):

		id=request.user.id

		c=Socia.objects.filter(user_id=id).values('id','nombre','apellido','photo','user__groups__name','correo','telefono','direccion','distrito__nombre')
		
		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")


class Miperfil(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self, request):


		grupos = Group.objects.get(user=request.user.id).name

		print 'gupo.....',grupos

		if grupos=='Socia':

			c=Socia.objects.filter(user_id=request.user.id).values('id','nombre','apellido','photo','user__groups__name','telefono','direccion','distrito__nombre','user__first_name','email')
		

		if grupos=='Cliente':

			c=Cliente.objects.filter(user_id=request.user.id).values('id','nombre','apellido','photo','user__groups__name','email','telefono','direccion','distrito__nombre','user__first_name')
		
		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")



class Miservicios(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self, request):

		id_cliente=Cliente.objects.get(user_id=request.user.id).id

		c= Servicio.objects.filter(cliente_id=id_cliente).values('id','cliente__nombre','dia__nombre','cliente__photo','socia__photo','socia__nombre','socia__nombre').order_by('-id')

		fmt = '%H:%M'

		fmt1= '%b-%d'

		for i in range(len(c)):

			print 'c[i][id]',c[i]['id']


			c[i]['fecha_inicio']= Servicio.objects.get(id=c[i]['id']).fecha_inicio.strftime(fmt)

			c[i]['fecha']= Servicio.objects.get(id=c[i]['id']).fecha.strftime(fmt1)

			sp=Serviciopedido.objects.filter(servicio_id=c[i]['id']).values('subcategoria__nombre','subcategoria__precio')

			c[i]['pedidos'] =ValuesQuerySetToDict(sp)


		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")

class Miserviciossocias(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self,request,socia):

		id_socia=Socia.objects.get(user_id=request.user.id).id

		c= Servicio.objects.filter(socia_id=id_socia).values('id','cliente__nombre','dia__nombre','cliente__photo','socia__photo','socia__nombre','socia__nombre').order_by('-id')

		fmt = '%H:%M'

		fmt1= '%b-%d'

		for i in range(len(c)):

			print 'c[i][id]',c[i]['id']


			c[i]['fecha_inicio']= Servicio.objects.get(id=c[i]['id']).fecha_inicio.strftime(fmt)

			c[i]['fecha']= Servicio.objects.get(id=c[i]['id']).fecha.strftime(fmt1)

			sp=Serviciopedido.objects.filter(servicio_id=c[i]['id']).values('subcategoria__nombre','subcategoria__precio')

			c[i]['pedidos'] =ValuesQuerySetToDict(sp)


		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")


class Detalleservicio(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self, request,servicio):

		c= Servicio.objects.filter(id=servicio).values('id','cliente__nombre','dia__nombre','cliente__photo','socia__photo','socia__nombre','socia__nombre','latitud','longitud').order_by('-id')

		fmt = '%H:%M'

		fmt1= '%b-%d'

		for i in range(len(c)):

			print 'c[i][id]',c[i]['id']


			c[i]['fecha_inicio']= Servicio.objects.get(id=c[i]['id']).fecha_inicio.strftime(fmt)

			c[i]['fecha']= Servicio.objects.get(id=c[i]['id']).fecha.strftime(fmt1)

			sp=Serviciopedido.objects.filter(servicio_id=c[i]['id']).values('subcategoria__nombre','subcategoria__precio')

			c[i]['pedidos'] =ValuesQuerySetToDict(sp)


		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")



class Ultimoservicio(JSONWebTokenAuthMixin, View):

	
	## Agrega telefonos
	def get(self, request):

		socia_id=Socia.objects.get(user_id=request.user.id)

		id_serv = Servicio.objects.all().values('id').order_by('-id')[0]['id']

		c= Servicio.objects.filter(id=id_serv,socia_id=socia_id).values('id','cliente__nombre','dia__nombre','cliente__photo','socia__photo','socia__nombre','socia__nombre','latitud','longitud').order_by('-id')

		fmt = '%H:%M'

		fmt1= '%b-%d'

		for i in range(len(c)):

			c[i]['fecha_inicio']= Servicio.objects.get(id=c[i]['id']).fecha_inicio.strftime(fmt)

			c[i]['fecha']= Servicio.objects.get(id=c[i]['id']).fecha.strftime(fmt1)

			sp=Serviciopedido.objects.filter(servicio_id=c[i]['id']).values('subcategoria__nombre','subcategoria__precio','subcategoria__categoria__icono')

			c[i]['pedidos'] =ValuesQuerySetToDict(sp)


		c= simplejson.dumps(ValuesQuerySetToDict(c))

		return HttpResponse(c, content_type="application/json")

class Buscasocia(JSONWebTokenAuthMixin, View):

	#Crea nuevo cliente
	def post(self,request,id_socia):

		print 'Buscando socias....'

		data = json.loads(request.body)


		pedidos =[]

		for p in data['pedido']:

			pedidos.append(p['id'])

		print 'Pedidos..',pedidos

		latitud = data['ubicacion']['lat']

		longitud = data['ubicacion']['long']

		reservado = str(data['hora'])

		referencia = str(data['referencia'])

		reservado = datetime.datetime.strptime(reservado, '%H:%M')

		reservado= str(reservado.strftime('%H:%M:%S'))

		dia = data['dia']



		xx=datetime.datetime.strptime(str(data['dia'])[0:10], '%Y-%m-%d')



		#ubicacion = data['reserva']['ubicacion']

		dia=dia[0:10]

		hora = reservado[0:2]

		minuto = reservado[3:5]

		segundo = reservado[6:8]

		hora_reserva =  hora+':'+minuto+'[:'+segundo+'[.000000]]'

		print 'hora_reserva',hora_reserva

		fecha=  datetime.datetime.strptime(str(dia), '%Y-%m-%d')

		dia = fecha.strftime("%a")

		print 'dia',dia

		if dia=='Sun': dia='Domingo'
		if dia=='Mon': dia='Lunes'
		if dia=='Tue': dia='Martes'
		if dia=='Wed': dia='Miercoles'
		if dia=='Thu': dia='Jueves'
		if dia=='Fri': dia='Viernes'
		if dia=='Sat': dia='Sabado'


		if dia=='Sabado':ndia=6
		if dia=='Viernes':ndia=5
		if dia=='Jueves':ndia=4
		if dia=='Miercoles':ndia=3
		if dia=='Martes':ndia=2
		if dia=='Lunes':ndia=1
		if dia=='Domingo':ndia=7

		cli = Cliente.objects.get(user_id=request.user.id).id

		query = reduce(operator.and_, (Q(subcategoria__id__contains = item) for item in pedidos))
		
		#{u'pedido': [{u'descripcion': u'ghghg<br> Costo: S/. 2.0', u'nombre': u'Manicure Express', u'precio': 2, u'id': 1, u'check': True}, {u'descripcion': u'<br> Costo: S/. 2.0', u'nombre': u'Manicure Spa', u'precio': 2, u'id': 2, u'check': True}]}

		sociascate=Sociasubcategoria.objects.filter(query)

		print 'Nuemros de Socias..',sociascate.count()

		Servicio(socia_id=1,referencia=referencia,dia_id=ndia,fecha_inicio=hora_reserva,cliente_id=cli,fecha=xx,latitud=latitud,longitud=longitud,estado_id=1).save()

		id_serv = Servicio.objects.all().values('id').order_by('-id')[0]['id']

		if sociascate.count()==0:


			subject, from_email, to = 'My Look Express', 'cotiza@hermes.pe', 'joelunmsm@gmail.com'
			
			text_content = 'Una cliente nueva no encontro una socia, porfavor apoyarle, en el siguiente link detalle su informacion: '

			text_content= text_content+'http://estokealo.com:8000/admin/app/serviciopedido/?servicio__id__exact='+str(id_serv)
			
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])


			msg.send()



		##Guarda pedidos subcategorias

		for p in data['pedido']:

			Serviciopedido(servicio_id=id_serv,subcategoria_id=p['id']).save()


		for s in sociascate:


			print 'Socia-Categoria',s

		
			t = Turnosocia.objects.filter(socia_id=s.socia.id,fecha_inicio__lte=hora_reserva,fecha_fin__gte=hora_reserva,dia__nombre=dia)

			### Envia notificacion a la socia

			if t.count()>0:

				print 'Socia encontrada..',s.socia.nombre,s.socia.numero_notificacion

				if s.socia.numero_notificacion:

					ser = Servicio.objects.get(id=id_serv)
					ser.socia_id=s.socia.id
					ser.save()

					header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic OGQyNTllMmUtMmY2Ny00ZGQxLWEzNWMtMjM5NTdlNjM0ZTc3"}
					payload = {"app_id": "6d06ccb5-60c3-4a76-83d5-9363fbf6b40a","include_player_ids": [s.socia.numero_notificacion],"contents": {"en": "Tienes un nuevo servicio requerido"},"data":{'servicio': id_serv}}
					req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
					print(req.status_code, req.reason)


					break

			else:

				subject, from_email, to = 'My Look Express', 'cotiza@hermes.pe', 'joelunmsm@gmail.com'

				text_content = 'Existen socias para este pedido pero no esta disponibles en este horario porfavor solucionar: '

				text_content= text_content+'http://estokealo.com:8000/admin/app/serviciopedido/?servicio__id__exact='+str(id_serv)

				msg = EmailMultiAlternatives(subject, text_content, from_email, [to])


				msg.send()



		return HttpResponse(simplejson.dumps('cliente_id'), content_type="application/json")


def categoria(request):

	c= Categoria.objects.all().values('id','nombre','photo','icono','icono_seleccionado').order_by('orden')

	for i in range(len(c)):

		c[i]['check']=True



	c= simplejson.dumps(ValuesQuerySetToDict(c))

	return HttpResponse(c, content_type="application/json")

@csrf_exempt
def nuevasocia(request):

	print 'entrando..'

	if request.method=='POST':


		cat = json.loads(request.body)['categoria']

		soc = json.loads(request.body)['socia']





		subject, from_email, to = 'My Look Express Nueva Socia', 'cotiza@hermes.pe', 'carloscano.e@gmail.com'
		text_content = 'Un nueva socia '
		

		html_content = ''

		for c in cat:

			html_content = html_content + ' <br> '+c['nombre']

		categoriastxt = html_content

		titulo = 'Estimado Carlos se solicito una nueva socia con los siguientes datos :<br><br> '


		nombre = 'Nombre: '+soc['nombre']+ ' <br>'
		telefono = 'Telefono '+soc['telefono']+ ' <br>'
		email ='Email '+soc['email']+'<br>'
		direccion='Direccion '+soc['direccion']+' <br>'

		html_content= titulo +nombre+telefono+email+direccion+ 'Categorias : <br> '+categoriastxt

		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		#msg.attach_file('/var/www/hermes/out.pdf')
		msg.attach_alternative(html_content, "text/html")
		msg.send()


	c= simplejson.dumps('67')

	return HttpResponse(c, content_type="application/json")



def detalledeservicio(request,id_servicio):

	print 'aqui toy'

	c= Servicio.objects.filter(id=id_servicio).values('id','cliente__nombre','dia__nombre','cliente__photo','socia__photo','socia__nombre','latitud','longitud')

	fmt = '%H:%M:%S'

	fmt1= '%Y-%m-%d'

	for i in range(len(c)):

		print 'latitud',c[i]['latitud']

		c[i]['fecha_inicio']= Servicio.objects.get(id=c[i]['id']).fecha_inicio.strftime(fmt)

		#c[i]['fecha']= Servicio.objects.get(id=c[i]['id']).fecha.strftime(fmt1)

		sp=Serviciopedido.objects.filter(servicio_id=c[i]['id']).values('subcategoria__nombre','subcategoria__precio','subcategoria__categoria__icono')

		c[i]['pedidos'] =ValuesQuerySetToDict(sp)


	c= simplejson.dumps(ValuesQuerySetToDict(c))

	return HttpResponse(c, content_type="application/json")



class Aceptarservicio(JSONWebTokenAuthMixin, View):

	#Crea nuevo cliente
	def post(self,request):


		print 'aceptaser',json.loads(request.body)[0]['id']

		id_socia=Socia.objects.get(user_id=request.user.id).id



		ser = Servicio.objects.get(id=json.loads(request.body)[0]['id'])

		numero_notificacion  = Cliente.objects.get(user_id=ser.cliente.user.id).numero_notificacion

		noticliente = ser.cliente.numero_notificacion

		ser.socia_id = id_socia

		ser.estado_id=2

		ser.save()

		header = {"Content-Type": "application/json; charset=utf-8","Authorization": "Basic OGQyNTllMmUtMmY2Ny00ZGQxLWEzNWMtMjM5NTdlNjM0ZTc3"}
		payload = {"app_id": "6d06ccb5-60c3-4a76-83d5-9363fbf6b40a","include_player_ids": [numero_notificacion],"contents": {"en": "Tienes una nueva chica que te atendera"},"data":{'aceptaservicio': json.loads(request.body)[0]['id']}}
		req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
		print(req.status_code, req.reason)

		x = {'servicio':json.loads(request.body)[0]['id'],'detalle':'socia-cliente'}

		c= simplejson.dumps(x)

		return HttpResponse(c, content_type="application/json")


def subcategoria(request,categoria):

	c= Subcategoria.objects.filter(categoria_id=categoria).values('id','nombre','descripcion','precio','photo').order_by('orden')

	for i in range(len(c)):

		c[i]['check']=False

		if c[i]['descripcion'] == None: c[i]['descripcion']= ''
		if c[i]['precio'] == None: c[i]['precio']= ''

		c[i]['descripcion']=c[i]['descripcion']


	c= simplejson.dumps(ValuesQuerySetToDict(c))

	return HttpResponse(c, content_type="application/json")

def distrito(request):

	c= Distrito.objects.all().values('id','nombre')

	c= simplejson.dumps(ValuesQuerySetToDict(c))

	return HttpResponse(c, content_type="application/json")

def portadaphoto(request):

	c= Portadaphoto.objects.all().values('id','nombre','photo')

	c= simplejson.dumps(ValuesQuerySetToDict(c))

	return HttpResponse(c, content_type="application/json")


class Guardanotificacion(JSONWebTokenAuthMixin, View):

	#Crea nuevo cliente
	def post(self, request):


		#serviciox = json.loads(json.loads(request.body)['data'])['notification']['payload']['additionalData']

		serviciox=json.loads(request.body)['notification']['payload']['additionalData']


		#{u'action': {u'type': 0}, u'notification': {u'displayType': 0, u'shown': True, u'isAppInFocus': True, u'androidNotificationId': -656582595, u'payload': {u'body': u'Tienes un nuevo servicio requerido', u'lockScreenVisibility': 1, u'fromProjectNumber': u'466431784640', u'rawPayload': u'{"google.sent_time":1514838068314,"custom":"{\\"a\\":{\\"servicio\\":128},\\"i\\":\\"f04fde66-1544-4070-a212-67ec007e3b82\\"}","from":"466431784640","alert":"Tienes un nuevo servicio requerido","google.message_id":"0:1514838068319696%65d63aedf9fd7ecd","notificationId":-656582595}', u'priority': 0, u'additionalData': {u'servicio': 128}, u'notificationID': u'f04fde66-1544-4070-a212-67ec007e3b82'}}}

		#c= simplejson.dumps('servicio')

		#return HttpResponse(c, content_type="application/json")

		for s in serviciox:

			print 'servicio..',s

			if s=='codigo':

				if Socia.objects.filter(user_id=request.user.id):

					so = Socia.objects.get(user_id=request.user.id)
					so.numero_notificacion = serviciox['codigo']
					so.save()

				if Cliente.objects.filter(user_id=request.user.id):

					cli = Cliente.objects.get(user_id=request.user.id)
					cli.numero_notificacion = serviciox['codigo']
					cli.save()


				c= simplejson.dumps('ok')

				return HttpResponse(c, content_type="application/json")


			if s=='servicio':

				servicio= serviciox['servicio']
				
				#Notificacion(descripcion=json.loads(request.body),fecha=datetime.datetime.today(),servicio_id=servicio).save()

				servicio = {'servicio':servicio,'detalle':'cliente-socia'}


				print 'entre...'
				c= simplejson.dumps(servicio)

				return HttpResponse(c, content_type="application/json")

			if s=='aceptaservicio':

				print 'aceptaservicio....',s

				servicio= json.loads(json.loads(request.body)['data'])['notification']['payload']['additionalData']['aceptaservicio']
				
				#Notificacion(descripcion=json.loads(request.body),fecha=datetime.datetime.today(),servicio_id=servicio).save()

				servicio = {'servicio':servicio,'detalle':'aceptaservicio'}

				c= simplejson.dumps(servicio)

				return HttpResponse(c, content_type="application/json")



