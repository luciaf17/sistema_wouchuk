import decimal
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from .models import Remito, DetalleRemito
from clientes.models import Cliente
from stock.models import Deposito
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
                        cantidad = detalle.get('cantidad')
                        precio_unit = detalle.get('precio_unit') or 0  # Si está vacío, asignar 0

                        # Verificar campos requeridos (sin validar precio_unit como obligatorio)
                        if not producto_id or not cantidad:
                            raise ValueError(f"Datos incompletos en detalle: {detalle}")

                        producto = Producto.objects.get(id=producto_id)

                        # Asignar depósitos automáticamente según tipo de remito
                        dep_origen = (
                            Deposito.objects.get(id=dep_origen_id)
                            if dep_origen_id
                            else None
                        )
                        dep_destino = (
                            Deposito.objects.get(id=dep_destino_id)
                            if dep_destino_id
                            else None
                        )

                        DetalleRemito.objects.create(
                            remito=self.object,
                            producto=producto,
                            dep_origen=dep_origen,
                            dep_destino=dep_destino,
                            cantidad=int(cantidad),
                            precio_unit=decimal.Decimal(precio_unit)
                        )
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
        tipo_remito = form.cleaned_data.get('tipo_remito')  # Obtener el tipo de remito
        response = super().form_valid(form)

        detalles_json = self.request.POST.get('detalles[]')
        if detalles_json:
            try:
                detalles = json.loads(detalles_json)
                with transaction.atomic():
                    # Eliminar detalles existentes antes de agregar nuevos
                    DetalleRemito.objects.filter(remito=self.object).delete()
                    for detalle in detalles:
                        producto_id = detalle.get('id')
                        dep_origen_id = detalle.get('dep_origen')
                        dep_destino_id = detalle.get('dep_destino')
                        cantidad = detalle.get('cantidad')
                        precio_unit = detalle.get('precio_unit') or 0  # Si está vacío, asignar 0

                        # Verificar campos requeridos
                        if not producto_id or not cantidad or not precio_unit:
                            raise ValueError(f"Datos incompletos en detalle: {detalle}")

                        producto = Producto.objects.get(id=producto_id)

                        # Asignar depósitos automáticamente según tipo de remito
                        dep_origen = (
                            Deposito.objects.get_or_create(descripcion="Compras")[0]
                            if tipo_remito == "compra"
                            else Deposito.objects.get(id=dep_origen_id) if dep_origen_id else None
                        )
                        dep_destino = (
                            Deposito.objects.get_or_create(descripcion="Ventas")[0]
                            if tipo_remito == "venta"
                            else Deposito.objects.get(id=dep_destino_id) if dep_destino_id else None
                        )

                        DetalleRemito.objects.create(
                            remito=self.object,
                            producto=producto,
                            dep_origen=dep_origen,
                            dep_destino=dep_destino,
                            cantidad=int(cantidad),
                            precio_unit=decimal.Decimal(precio_unit)
                        )
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





def remito_anular(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    remito.estado_remito = 'anulado'
    remito.save()
    return redirect('remito_list')


def remito_activar(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    remito.estado_remito = 'activo'
    remito.save()
    return redirect('remito_list')