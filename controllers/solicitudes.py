# -*- coding: utf-8 -*-

def index():
    redirect(URL('solicitudes'))
    return locals()

def agregar():
    form = SQLFORM( db.Solicitud, fields=['id','Especificacion','Status'] )
    if form.process().accepted:
        session.flash = T('La solicitud fue agregada exitosamente!')
        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('La forma tiene errores, por favor llenela correctamente.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()


def listar():
    if request.args(0) is None:
        filas = db(db.Solicitud).select(orderby=db.Material.id)
    elif request.args(0)=='id':
        filas = db(db.).select(orderby=db.Solicitud.id)
        response.flash = T('Los materiales fueron ordenados por cantidad.')
    elif request.args(0)=='nombre':
        filas = db(db.Solicitud).select(orderby=db.Solicitud.Nombre)
        response.flash = T('Los materiales fueron ordenados por nombre.')
    elif request.args(0)=='area':
        filas = db(db.Solicitud).select(orderby=db.Solicitud.Area)
        response.flash = T('Los materiales fueron ordenados por area.')
    return locals()


def modificar():
    record = db.Solicitud(request.args(0)) or redirect(URL('agregar'))
    form = SQLFORM(db.Solicitud, record)
    if form.process().accepted:
        response.flash = T('El material fue modificado exitosamente!')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()

