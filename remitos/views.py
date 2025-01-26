import decimal
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from .models import Remito, DetalleRemito
from clientes.models import Cliente
from stock.models import Deposito, Stock
from .forms import RemitoForm, DetalleRemitoForm
from django.forms import modelformset_factory
from django.db import transaction
from productos.models import Producto
import json
from django.http import JsonResponse
import os
from fpdf import FPDF
from django.utils.timezone import localtime
from math import ceil
from django.http import FileResponse
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Q

class RemitoListView(ListView):
    model = Remito
    template_name = 'remitos/remito_list.html'
    context_object_name = 'remitos'

    def get_queryset(self):
        queryset = Remito.objects.select_related('cliente').all()

        # Obtener los parámetros de filtro
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        cliente = self.request.GET.get('cliente')
        tipo_remito = self.request.GET.get('tipo_remito')
        producto = self.request.GET.get('producto')

        # Filtro por fecha desde (inicio del día)
        if fecha_desde:
            try:
                fecha_desde_dt = make_aware(datetime.strptime(fecha_desde, '%Y-%m-%d'))
                queryset = queryset.filter(fecha__gte=fecha_desde_dt)
            except ValueError:
                print(f"Fecha desde inválida: {fecha_desde}")

        # Filtro por fecha hasta (final del día)
        if fecha_hasta:
            try:
                fecha_hasta_dt = make_aware(datetime.strptime(fecha_hasta, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1))
                queryset = queryset.filter(fecha__lte=fecha_hasta_dt)
            except ValueError:
                print(f"Fecha hasta inválida: {fecha_hasta}")

        # Filtro por cliente
        if cliente:
            queryset = queryset.filter(cliente_id=cliente)

        # Filtro por tipo de remito
        if tipo_remito:
            queryset = queryset.filter(tipo_remito=tipo_remito)

        # Filtro por producto
        if producto:
            queryset = queryset.filter(detalleremito__producto__descripcion__icontains=producto).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()  # Lista de clientes para el filtro
        context['remito_tipos'] = dict(Remito._meta.get_field('tipo_remito').choices)  # Opciones del tipo de remito
        return context



def generar_pdf_remito(remito, detalles):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Configuración de fuentes
    pdf.set_font('Helvetica', 'B', 12)  # Fuente en negrita para títulos

    # Agregar el logo
    logo_path = "static/wouchuk-logo.jpg"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=33)  # Ajusta las coordenadas y el tamaño del logo
    else:
        print(f"Error: No se encontró el logo en la ruta {logo_path}")

    # Encabezado
    remito_id_formateado = f"{remito.id:08d}"  # Formatear con ceros a la izquierda
    pdf.cell(200, 10, f"Remito - #{remito_id_formateado}", ln=True, align="C")
    pdf.ln(10)

    # Detalles del remito
    pdf.set_font('Helvetica', '', 10)  # Fuente regular para detalles
    pdf.cell(200, 10, f"Fecha: {localtime(remito.fecha).strftime('%d/%m/%Y %H:%M')}", ln=True, align="R")
    pdf.cell(200, 10, f"Tipo: {remito.get_tipo_remito_display()}", ln=True, align="L")

    # Mostrar fantasía del cliente si existe
    cliente_fantasia = remito.cliente.fantasia if remito.cliente and remito.cliente.fantasia else "-"
    pdf.cell(200, 10, f"Cliente: {cliente_fantasia}", ln=True, align="L")

    # Verificar si hay número de comprobante asociado
    if remito.nro_comprobante_asoc:
        pdf.cell(200, 10, f"Nro Comprobante Asociado: {remito.nro_comprobante_asoc}", ln=True, align="L")
    
    pdf.ln(10)

    # Configuración de la tabla
    pdf.set_fill_color(0, 150, 0)  # Color verde para el encabezado
    pdf.set_text_color(255, 255, 255)  # Texto blanco para el encabezado
    pdf.set_font('Helvetica', 'B', 8)  # Fuente en negrita para encabezados
    pdf.cell(20, 10, "Código", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Barcode", border=1, align="C", fill=True)
    pdf.cell(70, 10, "Descripción", border=1, align="C", fill=True)
    pdf.cell(20, 10, "Cantidad", border=1, align="C", fill=True)
    pdf.cell(10, 10, "D.O", border=1, align="C", fill=True)
    pdf.cell(10, 10, "D.D", border=1, align="C", fill=True)
    pdf.cell(20, 10, "Precio Unit.", border=1, align="C", fill=True)
    pdf.ln()

    # Filas
    pdf.set_text_color(0, 0, 0)  # Texto negro para las filas
    pdf.set_font('Helvetica', '', 8)  # Fuente regular para las filas

    for detalle in detalles:
        pdf.cell(20, 10, str(detalle.producto.id), border=1, align="C")  # Código
        pdf.cell(40, 10, detalle.producto.barcode, border=1, align="C")  # Barcode
        pdf.cell(70, 10, detalle.producto.descripcion[:35], border=1, align="L")  # Descripción corta
        pdf.cell(20, 10, str(detalle.cantidad), border=1, align="C")  # Cantidad
        pdf.cell(10, 10, detalle.dep_origen.descripcion if detalle.dep_origen else "-", border=1, align="C")  # Depósito Origen
        pdf.cell(10, 10, detalle.dep_destino.descripcion if detalle.dep_destino else "-", border=1, align="C")  # Depósito Destino
        pdf.cell(20, 10, f"${detalle.precio_unit:.2f}", border=1, align="R")  # Precio Unitario
        pdf.ln()

    # Guardar PDF
    pdf_dir = "static/remitos"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    pdf_path = os.path.join(pdf_dir, f"remito_{remito_id_formateado}.pdf")
    pdf.output(pdf_path)
    return pdf_path


def actualizar_stock(producto, deposito, cantidad, tipo_remito, deposito_origen=None):
    """
    Actualiza el stock de un producto en un depósito según el tipo de remito.
    - tipo_remito: 'compra', 'venta', 'interdeposito', 'ajuste'.
    - deposito_origen: se usa para interdeposito y venta.
    """
    if tipo_remito == 'compra':
        # Restar del depósito "Compras"
        deposito_compras, _ = Deposito.objects.get_or_create(descripcion="Compras")
        stock_compras, created = Stock.objects.get_or_create(producto=producto, deposito=deposito_compras)
        stock_compras.cantidad -= cantidad
        stock_compras.save()

        # Sumar al depósito final
        stock_destino, created = Stock.objects.get_or_create(producto=producto, deposito=deposito)
        stock_destino.cantidad += cantidad
        stock_destino.save()

    elif tipo_remito == 'venta':
        # Restar del depósito de origen
        if deposito_origen:
            stock_origen, created = Stock.objects.get_or_create(producto=producto, deposito=deposito_origen)
            stock_origen.cantidad -= cantidad
            stock_origen.save()

        # Sumar al depósito "Ventas"
        stock_ventas, created = Stock.objects.get_or_create(producto=producto, deposito=deposito)
        stock_ventas.cantidad += cantidad
        stock_ventas.save()

    elif tipo_remito == 'interdeposito':
        if deposito_origen:
            # Restar del depósito de origen
            stock_origen, created = Stock.objects.get_or_create(producto=producto, deposito=deposito_origen)
            stock_origen.cantidad -= cantidad
            stock_origen.save()

        # Sumar al depósito de destino
        stock_destino, created = Stock.objects.get_or_create(producto=producto, deposito=deposito)
        stock_destino.cantidad += cantidad
        stock_destino.save()

    elif tipo_remito == 'ajuste':
        # Ajustar al valor exacto en el depósito especificado
        stock, created = Stock.objects.get_or_create(producto=producto, deposito=deposito)
        stock.cantidad = cantidad
        stock.save()


class RemitoCreateView(CreateView):
    model = Remito
    form_class = RemitoForm
    template_name = 'remitos/remito_form.html'

    def form_valid(self, form):
        tipo_remito = form.cleaned_data.get('tipo_remito')  # Obtener el tipo de remito
        response = super().form_valid(form)

        detalles_json = self.request.POST.get('detalles[]')
        if detalles_json:
            try:
                detalles = json.loads(detalles_json)
                with transaction.atomic():
                    for detalle in detalles:
                        producto_id = detalle.get('id')
                        dep_origen_id = detalle.get('dep_origen')
                        dep_destino_id = detalle.get('dep_destino')
                        cantidad = int(detalle.get('cantidad'))  # Convertir a entero
                        precio_unit = detalle.get('precio_unit') or 0  # Si está vacío, asignar 0

                        # Verificar campos requeridos
                        if not producto_id or not cantidad:
                            raise ValueError(f"Datos incompletos en detalle: {detalle}")

                        producto = Producto.objects.get(id=producto_id)

                        # Configurar depósitos según el tipo de remito
                        dep_origen = None
                        dep_destino = None
                        if tipo_remito == "compra":
                            dep_origen = Deposito.objects.get_or_create(descripcion="Compras")[0]
                            if not dep_destino_id:
                                raise ValueError("El depósito de destino es obligatorio para una compra.")
                            dep_destino = Deposito.objects.get(id=dep_destino_id)
                        elif tipo_remito == "venta":
                            if not dep_origen_id:
                                raise ValueError("El depósito de origen es obligatorio para una venta.")
                            dep_origen = Deposito.objects.get(id=dep_origen_id)
                            dep_destino = Deposito.objects.get_or_create(descripcion="Ventas")[0]
                        elif tipo_remito == "interdeposito":
                            if not dep_origen_id or not dep_destino_id:
                                raise ValueError("Los depósitos de origen y destino son obligatorios para interdepósito.")
                            dep_origen = Deposito.objects.get(id=dep_origen_id)
                            dep_destino = Deposito.objects.get(id=dep_destino_id)
                        elif tipo_remito == "ajuste":
                            if not dep_destino_id:
                                raise ValueError("El depósito de destino es obligatorio para un ajuste.")
                            dep_destino = Deposito.objects.get(id=dep_destino_id)

                        # Crear el detalle del remito
                        DetalleRemito.objects.create(
                            remito=self.object,
                            producto=producto,
                            dep_origen=dep_origen,
                            dep_destino=dep_destino,
                            cantidad=cantidad,
                            precio_unit=decimal.Decimal(precio_unit)
                        )

                        # Actualizar el stock según el tipo de remito
                        actualizar_stock(producto, dep_destino, cantidad, tipo_remito, deposito_origen=dep_origen)

            except (ValueError, json.JSONDecodeError, Deposito.DoesNotExist, Producto.DoesNotExist) as e:
                form.add_error(None, f"Error procesando detalles: {e}")
                return self.form_invalid(form)

        # Generar el PDF
        detalles_remito = DetalleRemito.objects.filter(remito=self.object)
        pdf_path = generar_pdf_remito(self.object, detalles_remito)

        # Almacenar el path del PDF para el template
        self.pdf_path = pdf_path
        return redirect(self.get_success_url())

    def get_success_url(self):
        if hasattr(self, 'pdf_path'):
            return f'/static/remitos/remito_{str(self.object.id).zfill(8)}.pdf'
        return reverse_lazy('remito_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['depositos'] = json.dumps(list(Deposito.objects.values('id', 'descripcion')), default=str)
        context['detalle_remito'] = json.dumps([], default=str)  # Siempre enviar una lista vacía
        return context


class RemitoUpdateView(UpdateView):
    model = Remito
    form_class = RemitoForm
    template_name = 'remitos/remito_form.html'

    def form_valid(self, form):
        tipo_remito = form.cleaned_data.get('tipo_remito')
        response = super().form_valid(form)

        detalles_json = self.request.POST.get('detalles[]')
        if detalles_json:
            try:
                detalles = json.loads(detalles_json)
                with transaction.atomic():
                    # Revertir el impacto de los detalles antiguos en el stock
                    self.revertir_stock_antiguo(tipo_remito)

                    # Procesar los nuevos detalles y actualizar el stock
                    self.procesar_nuevos_detalles(detalles, tipo_remito)

            except (ValueError, json.JSONDecodeError, Deposito.DoesNotExist, Producto.DoesNotExist) as e:
                form.add_error(None, f"Error procesando detalles: {e}")
                return self.form_invalid(form)

        # Generar el PDF
        detalles_remito = DetalleRemito.objects.filter(remito=self.object)
        pdf_path = generar_pdf_remito(self.object, detalles_remito)

        # Almacenar el path del PDF para el template
        self.pdf_path = pdf_path
        return redirect(self.get_success_url())

    def revertir_stock_antiguo(self, tipo_remito):
        """
        Revertir el impacto de los detalles antiguos en el stock.
        """
        detalles_antiguos = DetalleRemito.objects.filter(remito=self.object)

        for detalle in detalles_antiguos:
            if tipo_remito == 'compra':
                # Revertir compra
                actualizar_stock(detalle.producto, detalle.dep_destino, -detalle.cantidad, 'compra')
            elif tipo_remito == 'venta':
                # Revertir venta
                actualizar_stock(detalle.producto, detalle.dep_origen, detalle.cantidad, 'venta')
            elif tipo_remito == 'interdeposito':
                # Revertir interdepósito
                actualizar_stock(detalle.producto, detalle.dep_destino, -detalle.cantidad, 'interdeposito', deposito_origen=detalle.dep_origen)
            elif tipo_remito == 'ajuste':
                # Ajuste no requiere revertir
                continue

        # Eliminar los detalles antiguos
        detalles_antiguos.delete()

    def procesar_nuevos_detalles(self, detalles, tipo_remito):
        """
        Procesar y guardar los nuevos detalles, actualizando el stock.
        """
        for detalle in detalles:
            producto_id = detalle.get('id')
            dep_origen_id = detalle.get('dep_origen')
            dep_destino_id = detalle.get('dep_destino')
            cantidad = int(detalle.get('cantidad'))
            precio_unit = detalle.get('precio_unit') or 0

            producto = Producto.objects.get(id=producto_id)
            dep_origen = None
            dep_destino = None

            # Configurar depósitos según tipo de remito
            if tipo_remito == "compra":
                dep_origen = Deposito.objects.get_or_create(descripcion="Compras")[0]
                if not dep_destino_id:
                    raise ValueError("El depósito de destino es obligatorio para una compra.")
                dep_destino = Deposito.objects.get(id=dep_destino_id)
            elif tipo_remito == "venta":
                if not dep_origen_id:
                    raise ValueError("El depósito de origen es obligatorio para una venta.")
                dep_origen = Deposito.objects.get(id=dep_origen_id)
                dep_destino = Deposito.objects.get_or_create(descripcion="Ventas")[0]
            elif tipo_remito == "interdeposito":
                if not dep_origen_id or not dep_destino_id:
                    raise ValueError("Los depósitos de origen y destino son obligatorios para interdepósito.")
                dep_origen = Deposito.objects.get(id=dep_origen_id)
                dep_destino = Deposito.objects.get(id=dep_destino_id)
            elif tipo_remito == "ajuste":
                if not dep_destino_id:
                    raise ValueError("El depósito de destino es obligatorio para un ajuste.")
                dep_destino = Deposito.objects.get(id=dep_destino_id)

            # Crear detalle
            DetalleRemito.objects.create(
                remito=self.object,
                producto=producto,
                dep_origen=dep_origen,
                dep_destino=dep_destino,
                cantidad=cantidad,
                precio_unit=decimal.Decimal(precio_unit),
            )

            # Actualizar stock según el tipo de remito
            actualizar_stock(producto, dep_destino, cantidad, tipo_remito, deposito_origen=dep_origen)


    def get_success_url(self):
        if hasattr(self, 'pdf_path'):
            return f'/static/remitos/remito_{str(self.object.id).zfill(8)}.pdf'
        return reverse_lazy('remito_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['depositos'] = json.dumps(list(Deposito.objects.values('id', 'descripcion')), default=str)
        context['detalle_remito'] = json.dumps(list(
            DetalleRemito.objects.filter(remito=self.object).values(
                'producto__id', 'producto__descripcion', 'dep_origen__id', 'dep_destino__id', 'cantidad', 'precio_unit'
            )
        ), default=str)

        # Obtener cliente relacionado
        if self.object.cliente:
            context['cliente_data'] = {
                'id': self.object.cliente.id,
                'descripcion': self.object.cliente.descripcion,
                'fantasia': self.object.cliente.fantasia
            }
        else:
            context['cliente_data'] = None

        return context


def remito_activar(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    if remito.estado_remito == 'anulado':  # Solo activar si está anulado
        for detalle in remito.detalleremito_set.all():
            if remito.tipo_remito == 'compra':
                deposito_origen, _ = Deposito.objects.get_or_create(descripcion="Compras")
                actualizar_stock(detalle.producto, detalle.dep_destino, detalle.cantidad, 'compra', deposito_origen=deposito_origen)
            elif remito.tipo_remito == 'venta':
                deposito_destino, _ = Deposito.objects.get_or_create(descripcion="Ventas")
                if not detalle.dep_origen:
                    raise ValueError("El depósito de origen es obligatorio para activar una venta.")
                # Restar del depósito de origen
                actualizar_stock(detalle.producto, deposito_destino, detalle.cantidad, 'venta', deposito_origen=detalle.dep_origen)
            elif remito.tipo_remito == 'interdeposito':
                actualizar_stock(detalle.producto, detalle.dep_origen, -detalle.cantidad, 'interdeposito')
                actualizar_stock(detalle.producto, detalle.dep_destino, detalle.cantidad, 'interdeposito')
            elif remito.tipo_remito == 'ajuste':
                actualizar_stock(detalle.producto, detalle.dep_destino, detalle.cantidad, 'ajuste')

        remito.estado_remito = 'activo'
        remito.save()

    return redirect('remito_list')


def remito_anular(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    if remito.estado_remito != 'anulado':  # Solo anular si no está ya anulado
        for detalle in remito.detalleremito_set.all():
            if remito.tipo_remito == 'compra':
                deposito_origen, _ = Deposito.objects.get_or_create(descripcion="Compras")
                actualizar_stock(detalle.producto, detalle.dep_destino, -detalle.cantidad, 'compra', deposito_origen=deposito_origen)
            elif remito.tipo_remito == 'venta':
                deposito_ventas, _ = Deposito.objects.get_or_create(descripcion="Ventas")
                # Devolver al depósito de origen
                if not detalle.dep_origen:
                    raise ValueError("El depósito de origen es obligatorio para anular una venta.")
                actualizar_stock(detalle.producto, detalle.dep_origen, detalle.cantidad, 'venta', deposito_origen=detalle.dep_origen)
                # Restar del depósito de ventas
                actualizar_stock(detalle.producto, deposito_ventas, -detalle.cantidad, 'venta', deposito_origen=detalle.dep_origen)
            elif remito.tipo_remito == 'interdeposito':
                actualizar_stock(detalle.producto, detalle.dep_destino, -detalle.cantidad, 'interdeposito')
                actualizar_stock(detalle.producto, detalle.dep_origen, detalle.cantidad, 'interdeposito')
            elif remito.tipo_remito == 'ajuste':
                continue

        remito.estado_remito = 'anulado'
        remito.save()

    return redirect('remito_list')








    