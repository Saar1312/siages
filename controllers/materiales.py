# -*- coding: utf-8 -*-


def index():
    redirect(URL('listar'))
    return locals()


def agregar():
    form = SQLFORM( db.Materiales, fields=['Nombre','Especificacion','Unidad_de_Medida','Area',
                                           'Cantidad','Cantidad_Minima'] )
    if form.process().accepted:
        session.flash = T('El material fue agregado exitosamente!')
        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('La forma tiene errores, por favor llenela correctamente.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()


def listar():
    if request.args(0) is None:
        filas = db(db.Materiales).select(orderby=db.Materiales.id)
    elif request.args(0)=='cantidad':
        filas = db(db.Materiales).select(orderby=db.Materiales.Cantidad)
        response.flash = T('Los materiales fueron ordenados por cantidad.')
    elif request.args(0)=='nombre':
        filas = db(db.Materiales).select(orderby=db.Materiales.Nombre)
        response.flash = T('Los materiales fueron ordenados por nombre.')
    elif request.args(0)=='area':
        filas = db(db.Materiales).select(orderby=db.Materiales.Area)
        response.flash = T('Los materiales fueron ordenados por area.')
    return locals()


def modificar():
    record = db.Materiales(request.args(0)) or redirect(URL('agregar'))
    form = SQLFORM(db.Materiales, record)
    if form.process().accepted:
        response.flash = T('El material fue modificado exitosamente!')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()
