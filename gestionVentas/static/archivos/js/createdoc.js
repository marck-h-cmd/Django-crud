$(document).ready(function() {
    // Initialize select pickers
    $('.selectpicker').selectpicker();
    
    // Datepicker initialization
    $('.datepicker').datepicker({
        format: 'dd/mm/yyyy',
        language: 'es',
        autoclose: true
    });
    
    // Set default date to today
    $('#id_fecha_venta').val(new Date().toLocaleDateString('es-PE'));
    
    // Product change event
    $('#idproducto').change(function() {
        mostrarProducto();
    });
    
    // Client change event
    $('#idcliente').change(function() {
        mostrarCliente();
    });
    
    // Type change event
    $('#idtipo').change(function() {
        mostrarTipo();
    });
    
    // Add to cart button
    $('#btnadddet').click(function() {
        agregarDetalle();
    });

    // Validar cantidad en tiempo real
    $('#cantidad').on('input', function() {
        validarCantidad();
    });

    // Inicializar cálculos
    actualizarCalculos();
});

let cont = 0;
let total = 0;
let detalleventa = [];
const subtotal = [];
const controlproducto = [];

function mostrarCliente() {
    const id = $('#idcliente').val();
    if (!id) return;
    $.get(`/ventas/mostrarCliente/${id}/`, function(data) {
        $('#ruc').val(data.ruc_dni);
        $('#direccion').val(data.direccion);
    });
}

function mostrarProducto() {
    const idproducto = $('#idproducto').val();
    console.log("Producto seleccionado:", idproducto);
    if (idproducto && idproducto !== '0') {
        $.get(`/ventas/mostrarProducto/${idproducto}/`, function(data) {
            console.log("Datos del producto:", data);
            $('#unidad').val(data.unidad);
            $('#precio').val(data.precio);
            $('#stock').val(data.stock);
            
            // Mostrar información del stock
            mostrarStock(data.stock);
        });
    } else {
        // Ocultar información del stock si no hay producto seleccionado
        $('#stock-display').hide();
        $('#cantidad').val('');
        $('#precio').val('');
    }
}

function mostrarStock(stock) {
    console.log("Mostrando stock:", stock);
    const stockDisplay = $('#stock-display');
    const stockCantidad = $('#stock-cantidad');
    const stockWarning = $('#stock-warning');
    const stockMessage = $('#stock-message');
    
    stockCantidad.text(stock);
    stockDisplay.show();
    
    // Resetear clases
    stockCantidad.removeClass('stock-disponible stock-medio stock-bajo');
    stockWarning.hide();
    
    if (stock <= 0) {
        stockCantidad.addClass('stock-bajo');
        stockMessage.html('<i class="fas fa-exclamation-triangle"></i> Producto sin stock disponible');
        stockWarning.show();
    } else if (stock <= 5) {
        stockCantidad.addClass('stock-bajo');
        stockMessage.html('<i class="fas fa-exclamation-triangle"></i> Stock bajo - Quedan pocas unidades');
        stockWarning.show();
    } else if (stock <= 20) {
        stockCantidad.addClass('stock-medio');
        stockMessage.html('<i class="fas fa-exclamation-triangle"></i> Stock medio - Considere reabastecer pronto');
        stockWarning.show();
    } else {
        stockCantidad.addClass('stock-disponible');
    }
}

function validarCantidad() {
    const cantidad = parseFloat($('#cantidad').val()) || 0;
    const stock = parseFloat($('#stock').val()) || 0;
    const cantidadInput = $('#cantidad');
    
    if (cantidad > stock && stock > 0) {
        cantidadInput.addClass('is-invalid');
        // Mostrar tooltip de error si no existe
        if (!cantidadInput.attr('data-original-title')) {
            cantidadInput.attr('data-toggle', 'tooltip');
            cantidadInput.attr('data-placement', 'top');
            cantidadInput.attr('title', `Cantidad máxima disponible: ${stock}`);
            cantidadInput.tooltip();
        }
        cantidadInput.tooltip('show');
    } else {
        cantidadInput.removeClass('is-invalid');
        cantidadInput.tooltip('hide');
    }
}

function mostrarTipo() {
    const idtipo = $('#idtipo').val();
    if (idtipo) {
        $.get(`/ventas/mostrarTipo/${idtipo}/`, function(data) {
            if (Array.isArray(data) && data.length > 0) {
                $('#id_nrodoc').val(data[0].numeracion);
            }
        });
    }
}

function mostrarMensajeError(mensaje) {
    $('#error-text').text(mensaje);
    $('#error-message').removeClass('d-none').show();
    
    // Auto-hide después de 5 segundos
    setTimeout(function() {
        $('#error-message').fadeOut(function() {
            $(this).addClass('d-none');
        });
    }, 5000);
    
    // Scroll to top para mostrar el error
    $('html, body').animate({
        scrollTop: 0
    }, 500);
}

function agregarDetalle() {
    const ruc = $('#ruc').val();
    if (!ruc) {
        mostrarMensajeError("Por favor seleccione el Cliente");
        return false;
    }
    
    const idproducto = $('#idproducto').val();
    const productoDesc = $('#idproducto option:selected').text();
    if (idproducto === '0') {
        mostrarMensajeError("Por favor seleccione el Producto");
        return false;
    }
    
    const cantidad = parseFloat($('#cantidad').val()) || 0;
    const stock = parseFloat($('#stock').val()) || 0;
    
    if (cantidad <= 0) {
        mostrarMensajeError("Por favor ingrese cantidad del producto mayor a 0");
        return false;
    }
    
    if (stock <= 0) {
        mostrarMensajeError("No hay stock disponible para este producto");
        return false;
    }
    
    if (cantidad > stock) {
        mostrarMensajeError(`No se tiene tal cantidad de producto, solo hay ${stock} unidades disponibles`);
        return false;
    }
    
    const precio = parseFloat($('#precio').val()) || 0;
    if (precio <= 0) {
        mostrarMensajeError("Por favor ingrese precio de venta del producto");
        return false;
    }
    
    // Check for duplicate products
    if (controlproducto.includes(idproducto)) {
        mostrarMensajeError("No puede volver a vender el mismo producto");
        return false;
    }
    
    console.log("Valores a agregar:", {
        idproducto,
        productoDesc,
        cantidad: $('#cantidad').val(),
        precio: $('#precio').val(),
        stock: $('#stock').val(),
        unidad: $('#unidad').val()
    });
    
    // Add to cart
    const unidad = $('#unidad').val();
    const itemSubtotal = cantidad * precio;
    
    subtotal[cont] = itemSubtotal;
    controlproducto[cont] = idproducto;
    total += itemSubtotal;
    
    const fila = `
        <tr class="selected" id="fila${cont}">
            <td class="text-center">
                <button type="button" class="btn btn-danger btn-sm" onclick="eliminardetalle('${idproducto}', ${cont});" 
                        title="Eliminar producto">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </td>
            <td class="text-center">
                <input type="hidden" name="cod_producto[]" value="${idproducto}">
                <span class="badge badge-info">${idproducto}</span>
            </td>
            <td>
                <i class="fas fa-cube text-muted"></i> ${productoDesc}
            </td>
            <td>
                <input type="hidden" name="unidad[]" value="${unidad}">
                <span class="badge badge-secondary">${unidad}</span>
            </td>
            <td class="text-center">
                <input type="hidden" name="cantidad[]" value="${cantidad}">
                <span class="badge badge-primary">${cantidad}</span>
            </td>
            <td class="text-right">
                <input type="hidden" name="pventa[]" value="${precio}">
                <i class="fas fa-dollar-sign text-success"></i> ${precio.toFixed(2)}
            </td>
            <td class="text-right font-weight-bold">
                <i class="fas fa-calculator text-info"></i> ${itemSubtotal.toFixed(2)}
            </td>
        </tr>
    `;
    
    $('#detalles tbody').append(fila);
    detalleventa.push({
        codigo: idproducto,
        unidad: unidad,
        cantidad: cantidad,
        pventa: precio,
        subtotal: itemSubtotal
    });
    
    cont++;
    
    // Actualizar cálculos
    actualizarCalculos();
    limpiar();
    
    // Mostrar animación de éxito
    animarCampo('#detalles tbody tr:last-child');
}

function actualizarCalculos() {
    const tipoDocumento = $('#idtipo').val();
    const subtotalSinIGV = total;
    
    if (tipoDocumento == 1) { // Factura
        const igv = subtotalSinIGV * 0.18;
        const totalConIGV = subtotalSinIGV + igv;
        
        $('#subtotal_display').val(subtotalSinIGV.toFixed(2));
        $('#igv_display').val(igv.toFixed(2)).parent().show(); // Mostrar IGV
        $('#total').val(totalConIGV.toFixed(2));
    } else { // Boleta
        $('#subtotal_display').val(subtotalSinIGV.toFixed(2));
        $('#igv_display').val('0.00').parent().hide(); // Ocultar IGV
        $('#total').val(subtotalSinIGV.toFixed(2));
    }
    
    // Animar los campos
    animarCampo('#subtotal_display');
    animarCampo('#total');
}

$('#idtipo').change(function() {
    actualizarCalculos();
})

function animarCampo(selector) {
    $(selector).addClass('highlight');
    setTimeout(function() {
        $(selector).removeClass('highlight');
    }, 1000);
}

function limpiar() {
    $('#cantidad').val('');
    $('#precio').val('');
    $('#idproducto').val('0').trigger('change');
    $('#stock-display').hide();
    $('#cantidad').removeClass('is-invalid').tooltip('hide');
    
    // Actualizar selectpicker
    $('.selectpicker').selectpicker('refresh');
}

function eliminardetalle(codigo, index) {
    // Confirmar eliminación
    if (!confirm('¿Está seguro de eliminar este producto de la venta?')) {
        return;
    }
    
    // Restar del total
    total -= subtotal[index];
    
    // Remover fila con animación
    $('#fila' + index).fadeOut(function() {
        $(this).remove();
    });
    
    // Remover de arrays de control
    const pos = controlproducto.indexOf(codigo);
    if (pos !== -1) {
        controlproducto.splice(pos, 1);
        detalleventa.splice(pos, 1);
    }
    
    // Actualizar cálculos
    actualizarCalculos();
}

// Validación del formulario antes de enviar
$('#venta-form').on('submit', function(e) {
    if (detalleventa.length === 0) {
        e.preventDefault();
        mostrarMensajeError('Debe agregar al menos un producto a la venta');
        return false;
    }
    
    if (!$('#idcliente').val()) {
        e.preventDefault();
        mostrarMensajeError('Debe seleccionar un cliente para la venta');
        return false;
    }
    
    // Mostrar loading en el botón
    $('#btnRegistrar').html('<i class="fas fa-spinner fa-spin"></i> Procesando...').prop('disabled', true);
});

// Inicializar tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});