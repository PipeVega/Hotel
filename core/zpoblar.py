import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='cmontenegro',
        tipo='Cliente', 
        nombre='Carla', 
        apellido='Montenegro', 
        correo=test_user_email if test_user_email else 'cmontenegro@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='20.126.948-9',	
        direccion='1908 Calle 18 de Julio \nPuerto Montt \nChile', 
        subscrito=True, 
        imagen='perfiles/mujerjoven.jpg')

    crear_usuario(
        username='bjana',
        tipo='Administrador', 
        nombre='Bastián', 
        apellido='Jaña', 
        correo=test_user_email if test_user_email else 'bjana@gmail.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.879.585-2', 
        direccion='1806 Pasaje Parque Japonés, \nPunta Arenas \nChile', 
        subscrito=False, 
        imagen='perfiles/jovenhombre.jpg')

    crear_usuario(
        username='alejandrosuper',
        tipo='Superusuario',
        nombre='Alejandro',
        apellido='Smith.',
        correo=test_user_email if test_user_email else 'alejandrosuper@gmail.com',
        es_superusuario=True,
        es_staff=True,
        rut='12.283.985-6',
        direccion='1987 Av. Los Dominicos, Las Condes \nSantiago, RM \nChile',
        subscrito=False,
        imagen='perfiles/hombre.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Suite'},
        { 'id': 2, 'nombre': 'Simple'},
        { 'id': 3, 'nombre': 'Doble'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Suite" (6 habitaciones)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Suite Presidencial',
            'descripcion': 'La Suite Presidencial es la habitación más exclusiva y lujosa de nuestro hotel. Diseñada para ofrecer una experiencia de hospedaje excepcional, esta suite cuenta con una amplia sala de estar con elegantes muebles, una chimenea y vistas panorámicas a la ciudad. La zona de descanso incluye una cama king size con sábanas de algodón egipcio de alta calidad y un baño privado con tina de hidromasaje, ducha de lluvia y amenidades de lujo.',
            'precio': 1000000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/SuitePresidencial.jpeg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Suite Matrimonial',
            'descripcion': 'Preparada especialmente para parejas recién casadas, esta suite cuenta con una elegante cama king size con dosel, decoración romántica y un baño con tina de hidromasaje y ducha de lluvia. Además, incluye un espacio de estar con chimenea, TV de pantalla plana y un pequeño balcón privado con vistas a los jardines del hotel.',
            'precio': 550000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/SuiteMatrimonial.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Suite Ejecutiva',
            'descripcion': 'Diseñada para satisfacer las necesidades de los huéspedes de negocios, esta suite cuenta con una cómoda cama king, un amplio escritorio de trabajo, conexión a internet de alta velocidad y una zona de estar separada con sofá y sillón. El baño privado tiene ducha, tina y amenidades de lujo.',
            'precio': 600000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/SuiteEjecutiva.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Suite Familiar',
            'descripcion': 'Ideal para familias, esta suite ofrece una recámara principal con cama king y una segunda recámara con camas individuales. Tiene una sala de estar separada con sofá cama para acomodar a los niños. Incluye un baño completo, nevera y microondas para mayor comodidad.',
            'precio': 680000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/SuiteFamiliar.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Suite Panorámica',
            'descripcion': 'Con impresionantes vistas a la ciudad, esta suite cuenta con una amplia sala de estar y una recámara principal con cama king. El baño privado tiene una espectacular tina de hidromasaje junto a grandes ventanales. Además, tiene una terraza privada con muebles de exterior.',
            'precio': 750000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/SuitePanoramica.jpeg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Suite Deluxe',
            'descripcion': 'Esta suite de estilo contemporáneo ofrece una cómoda cama king, una acogedora sala de estar con chimenea y un escritorio de trabajo. El baño cuenta con una ducha de lluvia, tina y amenidades premium. Otras comodidades incluyen un minibar, cafetera y acceso a un lounge privado.',
            'precio': 800000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/SuiteDeluxe.jpeg'
        },

        # Categoría "Simple" (3 habitaciones)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Habitación Estándar',
            'descripcion': 'Ésta cómoda habitación cuenta con una cama queen size, una zona de estar con sillón, escritorio de trabajo y TV de pantalla plana. El baño privado tiene ducha y ofrece artículos de aseo básicos. Ideal para viajes de negocios o de placer.',
            'precio': 160000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/SimpleEstandar.jpeg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Habitación Superior',
            'descripcion': 'Con una decoración moderna y elegante, ésta habitación cuenta con una cama king size, área de descanso con sofá y mesa de café, y escritorio de trabajo. El baño privado incluye tina y ducha. Ofrece vistas a los jardines o a la ciudad.',
            'precio': 200000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/SimpleSuperior.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Habitación Deluxe',
            'descripcion': 'Habitación amplia y luminosa con cama king size, zona de estar con sillones, escritorio y TV de pantalla plana de gran tamaño. El baño privado cuenta con tina y ducha separadas. Incluye un balcón privado con muebles de exterior.',
            'precio': 240000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/SimpleDeluxe.jpeg'
        },

        # Categoría "Doble" (3 habitaciones)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Habitación Doble Estándar',
            'descripcion': 'Esta cómoda habitación cuenta con dos camas individuales, una zona de estar con sillón, escritorio de trabajo y TV de pantalla plana. El baño privado tiene ducha y ofrece artículos de aseo básicos. Ideal para viajes de negocios o de placer.',
            'precio': 300000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/DobleEstandar.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Habitación Doble Superior',
            'descripcion': 'Con una decoración moderna y elegante, esta habitación cuenta con dos camas queen size, área de descanso con sofá y mesa de café, y escritorio de trabajo. El baño privado incluye tina y ducha. Ofrece vistas a los jardines o a la ciudad.',
            'precio': 350000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/DobleSuperior.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Habitación Doble Deluxe',
            'descripcion': 'Habitación amplia y luminosa con dos camas queen size, zona de estar con sillones, escritorio y TV de pantalla plana de gran tamaño. El baño privado cuenta con tina y ducha separadas. Incluye un balcón privado con muebles de exterior.',
            'precio': 450000,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/DobleDeluxe.jpeg'
        },
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['21.076.564-1', '17.056.219-6']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Reservado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Disponible':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

