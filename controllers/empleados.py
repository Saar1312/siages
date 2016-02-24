# -*- coding: utf-8 -*-


def index():
    redirect(URL('listar'))
    return locals()


def agregar():
    form = SQLFORM(db.Empleado)
    if form.process().accepted:
        session.flash = T('El empleado fue agregado exitosamente!')
        redirect(URL('listar'))
    elif form.errors:
        response.flash = T('La forma tiene errores, por favor llenela correctamente.')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()


def listar():
    if request.args(0) is None:
        filas = db(db.Empleado).select(orderby=db.Empleado.id)
    elif request.args(0)=='nombre':
        filas = db(db.Empleado).select(orderby=db.Empleado.Nombre)
        response.flash = T('Los empleados fueron ordenados por nombre.')
    elif request.args(0)=='cargo':
        filas = db(db.Empleado).select(orderby=db.Empleado.Cargo)
        response.flash = T('Los empleados fueron ordenados por cargo.')
    elif request.args(0)=='experticia':
        filas = db(db.Empleado).select(orderby=db.Empleado.Experticia)
        response.flash = T('Los empleados fueron ordenados por experticia.')
    elif request.args(0)=='activos':
        filas = db(db.Empleado.Estado=='Activo').select()
        response.flash = T('Solo se muestran empleados activos.')
    elif request.args(0)=='inactivos':
        filas = db(db.Empleado.Estado=='Inactivo').select()
        response.flash = T('Solo se muestran empleados inactivos.')
    return locals()


def modificar():
    record = db.Empleado(request.args(0)) or redirect(URL('agregar'))
    form = SQLFORM(db.Empleado, record)
    if form.process().accepted:
        response.flash = T('El empleado fue modificado exitosamente!')
    else:
        response.flash = T('Por favor llene la forma.')
    return locals()
