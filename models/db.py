# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

db.define_table('empleadoArlyn',
   Field('nombre'),
   Field('apellido'),
   Field('identificador'),
   Field('cargo'),
   Field('tlf'),
   primarykey=['identificador'])

db.define_table('inventario',
   Field('material'),
   Field('cantidad','float'))

db.define_table('edificio',
   Field('nombre'),
   Field('nomenclatura'))

db.define_table('lugar',
   Field('edificio',db.edificio),
   Field('espacio'),
   Field('referencia'),
   Field('extension_tlf', 'integer'))

db.define_table('area',
   Field('nombre'),
   Field('nomenclatura'))

db.define_table('supervisor',
   Field('area', db.area),
   Field('nombre'),
   Field('apellido'),
   Field('identificador'),
   primarykey=['identificador'])

db.define_table('unidad',
   Field('nombre', unique='true'))

db.define_table('estatus_solicitud',
   Field('nombre_estatus',unique='true'))

db.define_table('prioridad',
   Field('nombre_prioridad',unique='true'))

db.define_table('espacio',
   Field('nombre_espacio',unique='true'))

################################################NUEVO###############################################
db.define_table('Solicitud',
                Field('id', unique=True, requires=IS_NOT_EMPTY() ),
                Field('Especificacion', type='text' ),
                Field('Status', requires=IS_EMPTY_OR(IS_IN_SET(['Disponible','Critico','No disponible'])) )
               )
################################################/NUEVO###############################################
db.define_table('Material',
                Field('id', unique=True, requires=IS_NOT_EMPTY() ),
                Field('Nombre', unique=True, requires=IS_NOT_EMPTY() ),
                Field('Especificacion', type='text' ),
                Field('Status', requires=IS_EMPTY_OR(IS_IN_SET(['Disponible','Critico','No disponible'])) ),
                Field('Unidad_de_Medida', requires=IS_EMPTY_OR(IS_IN_SET(['Metro','Centimetro','Litro','Galon',
                                                                          'Kilogramo','Pulgada','Libra','Pie','Otro'])) ),
                Field('Area', requires=IS_IN_SET(['Plomeria','Mantenimiento','Albañileria','Electricidad','Carpinteria','Otro']) ),
                Field('Cantidad', type='integer' ),
                Field('Cantidad_Minima', type='integer' )
               )
#############################################NUEVO##################################################
db.define_table('MaterialAsignado',
                Field('Material_id', db.Material.id ),
                Field('Solicitud_id', db.Solicitud.id ),
                Field('Cantidad', type='integer', requires=IS_NOT_EMPTY() )
               )

db.define_table('EmpleadoAsignado',
                Field('Empleado_id', db.Empleado.id ),
                Field('Solicitud_id', db.Solicitud.id )
               )
############################################/NUEVO###################################################
db.define_table('Empleado',
                Field('id', unique=True, requires=IS_NOT_EMPTY() ),
                Field('Nombre', requires=IS_NOT_EMPTY() ),
                Field('Cedula', type='double', unique=True ),
                Field('USBID', type='string'),
                Field('Correo', requires=IS_EMAIL(),comment='nombre@mail.com' ),
                Field('Telefono', requires=IS_MATCH('^\d{4}?[\s.-]?\d{7}$',
                error_message='No es un numero de telefono valido.'),comment='xxxx-xxxxxxx' ),
                Field('Cargo', requires=IS_IN_SET(['Supervisor','Obrero']) ),
                Field('Experticia', requires=IS_IN_SET(['Albañil','Plomero', 'Electricista', 'Carpintero']) ),
                Field('Estado', requires = IS_IN_SET(['Inactivo','Activo']) )
               )

db.supervisor.area.requires = IS_IN_DB(db, db.area.nombre)
db.lugar.edificio.requires = IS_IN_DB(db, db.edificio.nombre)
db.supervisor.area.requires = IS_IN_DB(db, db.area.id, '%(nombre)s')
db.lugar.edificio.requires = IS_IN_DB(db, db.edificio.id, '%(nombre)s')
db.espacio.nombre_espacio.requires = IS_NOT_EMPTY()
db.empleadoArlyn.nombre.requires = IS_NOT_EMPTY()
db.empleadoArlyn.apellido.requires = IS_NOT_EMPTY()
db.empleadoArlyn.identificador.requires = IS_NOT_EMPTY()
db.inventario.material.requires = IS_NOT_EMPTY()
db.inventario.cantidad.requires = IS_NOT_EMPTY()
db.edificio.nombre.requires = IS_NOT_EMPTY()
db.edificio.nomenclatura.requires = IS_NOT_EMPTY()
db.area.nombre.requires = IS_NOT_EMPTY()
db.area.nomenclatura.requires = IS_NOT_EMPTY()
db.supervisor.nombre.requires = IS_NOT_EMPTY()
db.supervisor.apellido.requires = IS_NOT_EMPTY()
db.supervisor.identificador.requires = IS_NOT_EMPTY()
db.supervisor.area.requires = IS_NOT_EMPTY()
db.unidad.nombre.requires = IS_NOT_EMPTY()
db.prioridad.nombre_prioridad.requires = IS_NOT_EMPTY()
db.estatus_solicitud.nombre_estatus.requires = IS_NOT_EMPTY()
db.area.nombre.requires = IS_NOT_IN_DB(db, db.area.nombre)
db.edificio.nombre.requires = IS_NOT_IN_DB(db, db.edificio.nombre)
db.unidad.nombre.requires = IS_NOT_IN_DB(db, db.unidad.nombre)

# Tabla base de datos para notificación a través de correo electrónico

db.define_table('emails',
    Field('correo',requires=IS_NOT_EMPTY()),
    Field('asunto',requires=IS_NOT_EMPTY()),
    Field('mensaje','text',requires=IS_NOT_EMPTY())
    )
