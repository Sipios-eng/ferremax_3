from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
import requests
from .forms import RegistrationForm
from .models import EstadoPedido, Producto,Pedido,Entrega,EstadoEntrega,Contact,Marca,TipoProducto,DetallePedido,HistorialPrecios
from django.contrib.auth.decorators import login_required
from .cart import Cart
import json
import http.client
import mercadopago
from django.db.models import Q
import pandas as pd
import plotly.graph_objects as go
from xhtml2pdf import pisa
from django.template.loader import get_template

def index(request):
    return render(request, 'index.html')

def auth_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Correo o Contraseña incorrecta!'
            return render(request, 'auth_login.html', {'error': error})
    else:
        return render(request, 'auth_login.html')
    
def auth_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ingresado ya existe')
                messages.get_messages(request).used = True
                return redirect('auth_register')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo ingresado ya existe')
                messages.get_messages(request).used = True
                return redirect('auth_register')
            User.objects.create_user(username=username, first_name=name, last_name=last_name, password=password, email=email)
            return redirect('auth_login')
        else:
            messages.error(request, 'Error en el registro. Por favor, corrija los campos resaltados.')
            messages.get_messages(request).used = True
    else:  # GET request or any other method
        form = RegistrationForm()
    
    return render(request, 'auth_register.html', {'form': form}) 

def exit(request):
    logout(request)
    return redirect('auth_login')

def stock_products(request):
    productos = Producto.objects.all()

    if not productos:
        messages.error(request,'No existen productos registrados')
        messages.get_messages(request).used = True

    return render(request,'stock_products.html',{'productos':productos})

def pedidos(request):
    pedidos = Pedido.objects.all()
    estados_pedidos = []
 #Agregar al html botones para aprobar o rechazar pedidos. 
    for pedido in pedidos:
        # Acceder al nombre del estado del pedido para cada pedido
        estado_pedido = pedido.estado.estado
        estados_pedidos.append(estado_pedido)
    if not pedidos:
        messages.error(request,'No existen pedidos')
        messages.get_messages(request).used = True

    return render(request,'pedidos.html',{'pedidos':pedidos,'estados':estados_pedidos})

def solicitud_bodega(request):
    return render(request,'solicitud_bodega.html')



def productos(request):
    tipo_producto_id = request.GET.get('tipo_producto')
    productos = Producto.objects.all()
    categoria = None
    
    if tipo_producto_id:
        try:
            tipo_producto_id = int(tipo_producto_id)
            categoria = Producto.objects.filter(tipo_producto_id=tipo_producto_id)
        except ValueError:
            pass  # Si no es un entero, no hace nada adicional
    
    # Si hay una categoría seleccionada, usa esa, si no, usa todos los productos
    productos_a_mostrar = productos if categoria is None else categoria

    # Paginación: Número de productos por página (por ejemplo, 9)
    paginator = Paginator(productos_a_mostrar, 6)
    page_number = request.GET.get('page')  # Número de página actual desde la URL
    page_obj = paginator.get_page(page_number)

    tipos_producto = TipoProducto.objects.all()
    
    context = {
        'page_obj': page_obj,  # Página con los productos paginados
        'tipos_producto': tipos_producto,
        'categoria_actual': tipo_producto_id if categoria else None,
    }
    return render(request, 'productos.html', context)




@login_required
def cart(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    productoCart = cart.get_prodss()
    total = cart.cart_total()
    cantidad = cart.get_quants 
    userId = request.user
    ##clave produccion de usuario de prueba TESTUSER1085505293 pass : Hb9QJvAszT || revisar cuenta mercado pago siempre si tiene saldo
    sdk = mercadopago.SDK("APP_USR-170340208437871-051617-b45127860d141be852b0d15af556090e-1817032202")
    items = []

    for product_id, details in productoCart.items():
        product = details['product']

        try:
            quantity = details['quantity']
            unit_price = float(details['precio'])*1000
        except (ValueError, TypeError) as e:
            print(f"Error en conversión de cantidad o precio: {e}")
            continue 

        items.append({
            "title": product.nombre,  # Asumiendo que tu modelo Producto tiene un campo nombre
            "quantity": quantity,
            "unit_price": unit_price,
        })
        #Crear objeto de pedido en el for de items con estado pendiente, Agregar formulario de fecha a la tabla entrega y html (Crear formulario y dejar como defecto el estado de entrega por confirmar (?) )
    preference_data = {
        "back_urls": {
            "success": "http://127.0.0.1:8000/success_pay/",
        },
        "items": items
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]    
    #Creacion de objeto para estado pedido 
    for item in items:
        pedidoObj = Pedido(
            User=userId,
            nombre=item["title"],
            estado=EstadoPedido.objects.get(id=1),
            cantidad_producto=item["quantity"],
            precio_producto=item["unit_price"]
        )
        pedidoObj.save()

    return render(request,'cart.html',{'productos':cart_products,'preference':preference,'items':cantidad,'total':total})


def entrega(request):
    entregaObj = Entrega.objects.all()
    pedidoList = []
    estados = []
    estadoEntregaObj = EstadoEntrega.objects.all()

    for entrega in entregaObj:
        # Obtener el pedido asociado a esta entrega
        pedido = entrega.pedido   
        pedidoList.append(pedido)
        # Obtener el estado de entrega y agregarlo a la lista de estados
        estadoEntrega = entrega.estado_entrega.estado 
        estados.append(estadoEntrega)

    if not entregaObj:
        messages.error(request,'No existen registros de entrega')
        messages.get_messages(request).used = True

    if not pedidoList:
        messages.error(request,'No existen registros de pedidos') 
        messages.get_messages(request).used = True

    return render(request,'entrega.html',{'estado': estados, 'pedidos': pedidoList,'entrega':entregaObj,'estadoEntrega':estadoEntregaObj})


def edit_entrega(request,id_entrega):
    entregaObj = get_object_or_404(Entrega, id_entrega=id_entrega)
    detail = Entrega.objects.get(id_entrega=entregaObj.id_entrega)
    pedidoObj = Pedido.objects.get(id=detail.id_entrega)
    estadoEntregaObj = EstadoEntrega.objects.all()

    if not detail:
        messages.error(request,'No existen registros de entrega')
        messages.get_messages(request).used = True

    if not pedidoObj:
        messages.error(request,'No existen registros de pedidos') 
        messages.get_messages(request).used = True

    if request.method == 'POST':
        estado_id = request.POST.get('estado')
        pkEstado = EstadoEntrega.objects.get(id=estado_id)
        entregaObj.estado_entrega = pkEstado
        entregaObj.save()
        messages.success(request, 'Entrega registrada correctamente')
        messages.get_messages(request).used = True
        return redirect('entrega')
    else:
        return render(request,'editar_entrega.html',{'pedidos': pedidoObj,'entrega':entregaObj,'estadoEntrega':estadoEntregaObj})
    
#agregar producto a la sesion
def agregar_producto(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productoId'))
        product = get_object_or_404(Producto, id=product_id)
        cart.add(product=product)
        # response = JsonResponse({'Product name': product.nombre})

        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})

        return response 
       
#actualizar producto a la sesion    
def update_producto(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productoId'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity=product_qty)
        response = JsonResponse({'cantidadProd':product_qty})     
        return response
    
#eliminar producto de la sesion 
def delete_producto(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productoId'))
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})

    return response



def verProducto(request, producto_id):
    producto = Producto.objects.get(id = producto_id)
    if request.method == 'POST':    
        response = obtenerValoresApi(request,producto)
        data = json.loads(response.content.decode('utf-8'))
        nuevo_precio = data.get('nuevo_precio')

        return render(request, 'producto.html',{'producto':producto,'nuevo_precio':nuevo_precio})
    else:
        return render(request, 'producto.html',{'producto':producto})
    
def contact(request):
    producto = Producto.objects.all()

    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        productoId = request.POST.get('productoId', '').strip()
        comment = request.POST.get('comment', '').strip()

        # Validar que el producto haya sido seleccionado
        if not productoId or productoId == "Selecciona un producto":
            messages.error(request, 'Por favor, selecciona un producto antes de enviar el formulario.')
            return render(request, 'contact.html', {'producto': producto})

        try:
            # obtener el producto de id
            productObj = Producto.objects.get(id=productoId) 
        except Producto.DoesNotExist:
            messages.error(request, 'Producto seleccionado no es válido.')
            return render(request, 'contact.html', {'producto': producto})

        contact = Contact(
            motivo=motivo,
            producto=productObj,
            usuario=request.user,
            comentario=comment,
        )
        contact.save()
        messages.success(request, 'Registro añadido correctamente')
        messages.get_messages(request).used = True
        return redirect('contact')
    else:
        return render(request, 'contact.html',{'producto':producto})

def consulta_cliente(request):
    consultas = Contact.objects.all()
    if request.method == 'POST':
        respuesta = request.POST['respuesta']
        contact_id = request.POST['contact_id']
        contact = Contact(
            respuesta = respuesta
        )
        contact = get_object_or_404(Contact, id=contact_id)
        contact.respuesta = respuesta
        contact.save()

    return  render(request, 'consultas_cliente.html',{'data':consultas})

def mis_consultas(request,user_id):
    userObj = User.objects.get(id=user_id)
    data = Contact.objects.filter(usuario= userObj)

    return render(request,'mis_consultas.html',{'data':data})

def obtenerValoresApi(request, producto):
    nuevo_precio = None
    if request.method == 'POST':
        tipo_moneda = request.POST.get('tipo_moneda')
        producto_id = request.POST.get('producto_id')
        productObj = Producto.objects.get(id=producto_id)

        # Consumo de la API
        url = "mindicador.cl"
        connection = http.client.HTTPSConnection(url)
        connection.request('GET', '/api')
        response = connection.getresponse()
        
        if response.status != 200:
            return JsonResponse({'error': 'Error al conectar con la API'}, status=500)
        
        data = json.loads(response.read().decode('utf-8'))
        
        # Variables para almacenar los valores de las monedas
        dolar = data.get('dolar', {}).get('valor')
        uf = data.get('uf', {}).get('valor')
        euro = data.get('euro', {}).get('valor')
        utm = data.get('utm', {}).get('valor')

        # Verificar que los valores no sean None antes de hacer la conversión
        if tipo_moneda == 'dolar' and dolar is not None:
            nuevo_precio = round(float(producto.precio) / float(dolar), 3)  # Redondear a 3 decimales
        elif tipo_moneda == 'uf' and uf is not None:
            nuevo_precio = round(float(producto.precio) / float(uf), 3)  # Redondear a 3 decimales
        elif tipo_moneda == 'euro' and euro is not None:
            nuevo_precio = round(float(producto.precio) / float(euro), 3)  # Redondear a 3 decimales
        elif tipo_moneda == 'utm' and utm is not None:
            nuevo_precio = round(float(producto.precio) / float(utm), 3)  # Redondear a 3 decimales
        else:
            nuevo_precio = productObj.precio
        
        response_data = {'nuevo_precio': nuevo_precio}
        print("Datos de respuesta:", response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def success_pay(request):
    collection_id = request.GET.get('collection_id')
    collection_status = request.GET.get('collection_status')
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    payment_type = request.GET.get('payment_type')
    merchant_order_id = request.GET.get('merchant_order_id')
    preference_id = request.GET.get('preference_id')
    site_id = request.GET.get('site_id')
    processing_mode = request.GET.get('processing_mode')
    merchant_account_id = request.GET.get('merchant_account_id') 

    context = {
        'collection_id': collection_id,
        'collection_status': collection_status,
        'payment_id': payment_id,
        'status': status,
        'external_reference': external_reference,
        'payment_type': payment_type,
        'merchant_order_id': merchant_order_id,
        'preference_id': preference_id,
        'site_id': site_id,
        'processing_mode': processing_mode,
        'merchant_account_id': merchant_account_id,
    }


    return render(request,'success_pay.html',context)    

def obtener_datos_api(request):

    if request.method == 'POST':
        if 'FormProducto' in request.POST:    
            url = 'https://localhost:7249/api/Producto'
            headers = {'accept': '*/*'}

            response = requests.get(url, headers=headers, verify=False) 
            if response.status_code == 200:
                datos = response.json()

                for item in datos:
                    marcaObj = Marca.objects.get(id=item['marca_id'])
                    tipoProdObj = TipoProducto.objects.get(id=item['tipoProducto_id'])     
                    Producto.objects.create(
                        nombre=item['nombre'],
                        precio=item['precio'],
                        cantidad_disponible=item['cantidad_disponible'],
                        descripcion = item['descripcion'],
                        imagen_url = item['imagen_url'],
                        marca = marcaObj,
                        tipo_producto = tipoProdObj)
            messages.success(request, 'Productos añadidos correctamente')
            messages.get_messages(request).used = True                            
        elif 'FormMarca' in request.POST:
            url = 'https://localhost:7249/api/Marcas' 
            headers = {'accept': '*/*'}

            response = requests.get(url, headers=headers, verify=False) 
            if response.status_code == 200:
                datos = response.json()

                for item in datos:
                    Marca.objects.create(
                            nombre = item['nombre']
                            )
            messages.success(request, 'Marcas añadidas correctamente')
            messages.get_messages(request).used = True          
        elif 'FormTipoProducto' in request.POST:
           url = 'https://localhost:7249/api/TipoProducto'
           headers = {'accept': '*/*'}

           response = requests.get(url, headers=headers, verify=False) 
           if response.status_code == 200:
                datos = response.json()

                for item in datos:
                    TipoProducto.objects.create(
                            nombre = item['nombre']
                            )
                messages.success(request, 'Categorias añadidas correctamente')
                messages.get_messages(request).used = True                              
    else:
        datos = ''    
    return render(request, 'getApi.html')    

def registrar_entrega(request):
    pedidos = Pedido.objects.all()
    estados = EstadoEntrega.objects.all()

    if request.method == 'POST':
        fecha = request.POST.get('fecha_entrega')
        pedido_id = request.POST.get('pedido')
        estado_entrega_id = request.POST.get('estado_entrega')

        pedido = get_object_or_404(Pedido, id=pedido_id)
        estado_entrega = get_object_or_404(EstadoEntrega, id=estado_entrega_id)

        # Verificar si ya existe una entrega para este pedido
        entrega_existente = Entrega.objects.filter(pedido=pedido).first()

        if entrega_existente:
            # Si ya existe una entrega, actualizarla en lugar de crear una nueva
            entrega_existente.fecha_entrega = fecha
            entrega_existente.estado_entrega = estado_entrega
            entrega_existente.save()
            messages.success(request, 'Entrega actualizada correctamente')
        else:
            # Si no existe una entrega, crear una nueva
            entrega_obj = Entrega(
                pedido=pedido,
                fecha_entrega=fecha,
                estado_entrega=estado_entrega
            )
            entrega_obj.save()
            messages.success(request, 'Entrega registrada correctamente')

        return redirect('entrega')

    return render(request, 'registrarEntrega.html', {'pedidos': pedidos, 'estados': estados})

#eliminar pedidos 
def eliminar_pedido(request,pedido_id):
    pedidoObj = get_object_or_404(Pedido, id=pedido_id)
    estadoPRechazado = EstadoPedido.objects.get(id=4)

    if not pedidoObj:
        messages.error(request,'No existen pedidos registrados') 
        messages.get_messages(request).used = True   
    else:
        pedidoObj.estado = estadoPRechazado
        pedidoObj.save()
        messages.success(request,'Se rechazo el pedido correctamente!') 
        messages.get_messages(request).used = True 
        redirect('pedidos')    
    return render(request,'pedido_eliminado.html')    

#aceptar pedido 
def aceptar_pedido(request,pedido_id):
    pedidoObj = get_object_or_404(Pedido, id=pedido_id)
    estadoPAprobado = EstadoPedido.objects.get(id=3)

    if not pedidoObj:
        messages.error(request,'No existen pedidos registrados') 
        messages.get_messages(request).used = True   
    else:
        pedidoObj.estado = estadoPAprobado
        pedidoObj.save()
        messages.success(request,'Se Aprobó el pedido correctamente!') 
        messages.get_messages(request).used = True 
        redirect('pedidos')    
    return render(request,'pedido_aceptado.html')    

def add_product(request):
    tipoProducto = TipoProducto.objects.all()
    marca = Marca.objects.all()

    if request.method == 'POST':
        nombreP = request.POST.get('nombreProducto') 
        descripcionP = request.POST.get('descripcionProducto') 
        precioP = request.POST.get('precio') 
        cantidadP = request.POST.get('cantidad')  
        imagenP = request.POST.get('imagenP')  
        marcaP = request.POST.get('marcaP')  
        tipoproductoP = request.POST.get('categoriaP')  

        # Validación específica para la categoría
        if not tipoproductoP or tipoproductoP == "Selecciona una categoria":
            messages.error(request, 'Error: Debe seleccionar una categoría válida para el producto.')
            return render(request, 'add_producto.html', {'marca': marca, 'categoria': tipoProducto})

        # Validación del resto de los campos
        if not marcaP:
            messages.error(request, 'Error: Debe seleccionar una marca válida para el producto.')
            return render(request, 'add_producto.html', {'marca': marca, 'categoria': tipoProducto})

        # Obtención de los objetos relacionados y creación del producto
        marcaObj = get_object_or_404(Marca, id=marcaP)
        categoria = get_object_or_404(TipoProducto, id=tipoproductoP)
        
        productoObj = Producto.objects.create(
            nombre=nombreP,
            descripcion=descripcionP,
            precio=precioP,
            cantidad_disponible=cantidadP,
            imagen_url=imagenP,
            marca=marcaObj,
            tipo_producto=categoria 
        )
        
        messages.success(request, 'Producto añadido correctamente!')
        messages.get_messages(request).used = True  
        return redirect('agregar_producto')

    return render(request, 'add_producto.html', {'marca': marca, 'categoria': tipoProducto})


def delete_product(request):
    producto = Producto.objects.all()
    tipoproducto = TipoProducto.objects.all()

    return render(request,'delete_producto.html',{'producto':producto,'tipoproducto':tipoproducto})

def borrar_producto(request,producto_id):
    productoObj = get_object_or_404(Producto,id=producto_id)
    producto = Producto.objects.all()

    if not productoObj:
        messages.error(request,'No existen el producto registrado') 
        messages.get_messages(request).used = True   
    else:
        productoObj.delete()
        messages.success(request,'Se elimino el producto correctamente!') 
        messages.get_messages(request).used = True 
        redirect('eliminar_producto')  

    return render(request,'delete_producto.html',{'producto':producto})

def borrar_multiples_productos(request):
    if request.method == "POST":
        productos_seleccionados = request.POST.getlist('productos')  # Obtener lista de productos seleccionados
        if productos_seleccionados:
            Producto.objects.filter(id__in=productos_seleccionados).delete()
            messages.success(request, "Productos eliminados con éxito.")
            messages.get_messages(request).used = True   
        else:
            messages.error(request, "No se seleccionó ningún producto para eliminar.")
            messages.get_messages(request).used = True   
    return redirect('eliminar_producto')

def buscar_productos(request):
    query = request.GET.get('nombre')

    if query:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(marca__nombre__icontains=query) |
            Q(tipo_producto__nombre__icontains=query)
        )
    else:
        productos = None

    context = {
        'productos': productos,
        'query': query,
    }
    return render(request, 'search.html', context)

def eliminar_categorias(request):
    if request.method == "POST":
        categorias = request.POST.get('categorias')
        TipoProducto.objects.filter(id__in=categorias).delete()
        messages.success(request, "Categoria eliminada con éxito.")
        messages.get_messages(request).used = True 
        return redirect('eliminar_producto')  
    else:
         messages.error(request, "No se seleccionó ningúna categoria para eliminar.")
         messages.get_messages(request).used = True     

    return redirect('eliminar_producto')

def actualizar_producto(request):
    productosObj = Producto.objects.all()

    context = {
        'producto': productosObj
    }
    return render(request,'update_producto.html', context)

def edit_producto(request,id_producto):
    productoObj = get_object_or_404(Producto, id=id_producto)
    marcaObj = Marca.objects.all()
    categoriaObj = TipoProducto.objects.all()

    context = {
        'producto': productoObj,
        'marca':marcaObj ,
        'categoria':categoriaObj
    }


    if request.method == 'POST':
        nombreProducto = request.POST['nombreProducto']
        descripcionProducto = request.POST['descripcionProducto']
        precioProducto = request.POST['precio']
        cantidadProducto = request.POST['cantidad']
        imagenProducto = request.POST['imagenP']
        marcaID = request.POST['marcaP']
        categoriaID = request.POST['categoriaP']

        try:
            marcaObj = Marca.objects.get(id=marcaID)
            categoriaObj = TipoProducto.objects.get(id=categoriaID)
        except (Marca.DoesNotExist, TipoProducto.DoesNotExist):
            messages.error(request, "Marca o categoría no válida.")
            return redirect('edit_producto', id_producto=id_producto)
        
        productoObj.nombre = nombreProducto
        productoObj.descripcion = descripcionProducto
        productoObj.precio = precioProducto
        productoObj.cantidad_disponible = cantidadProducto
        productoObj.imagen_url = imagenProducto
        productoObj.marca = marcaObj  
        productoObj.tipo_producto = categoriaObj  

        productoObj.save()

        #Guardar historial de precio 
        HistorialPrecios.objects.create(
            producto=productoObj,
            precio = precioProducto
        )


        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('edit_producto',id_producto=id_producto) 

    return render(request,'editar_producto.html',context)

def historialPrecios(request,id_producto):
    ProductoObj = get_object_or_404(Producto,id=id_producto)
    data = {
        'Producto':[],
        'Precio':[],
        'Fecha':[]
    }

    for i in ProductoObj.precios.all():
        data['Producto'].append(ProductoObj.nombre)
        data['Precio'].append(i.precio)
        data['Fecha'].append(i.fecha)
    
    df = pd.DataFrame(data)

    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Ordenar los datos por fecha
    df.sort_values('Fecha', inplace=True)
    
    # Gráfico de historial de precios utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Precio'],
                             mode='lines+markers',
                             name=ProductoObj.nombre,
                             line=dict(color='blue', width=2),
                             marker=dict(size=8)))
    
    fig.update_layout(title=f'Historial de Precios para {ProductoObj.nombre}',
                      xaxis_title='Fecha',
                      yaxis_title='Precio',
                      hovermode='x unified')
    
    # Convertir el gráfico a HTML
    graph_html = fig.to_html(full_html=False)

    return render(request,'historialPrecios.html',{'grafico':graph_html,'Producto':ProductoObj})

def exportarPdf(request, id_producto):
    ProductoObj = get_object_or_404(Producto, id=id_producto)
    precios = ProductoObj.precios.all()

    # Crear una lista con los datos de precio y fecha
    data = {
        'Producto': ProductoObj.nombre,
        'Precios': [(p.fecha, p.precio) for p in precios]
    }

    template_path = 'historialPrecios_pdfTemplate.html'  
    context = {'Producto': ProductoObj, 'Precios': data}

    # Configurar la respuesta del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_{ProductoObj.nombre}.pdf"'

    # Renderizar el template
    template = get_template(template_path)
    html = template.render(context)
    
    # Generar el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar si hay errores en la generación
    if pisa_status.err:
        return HttpResponse(f'Error al generar PDF: {pisa_status.err}', status=400)

    return response


