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
    $('#producto_id').change(function() {
        mostrarProducto();
    });
    
    // Client change event
    $('#id_idcliente').change(function() {
        mostrarCliente();
    });
    
    // Type change event
    $('#id_tipo').change(function() {
        mostrarTipo();
    });
    
    // Add to cart button
    $('#btnadddet').click(function() {
        agregarDetalle();
    });
});

var cont = 0;
var total = 0;
var detalleventa = [];
var subtotal = [];
var controlproducto = [];

function mostrarCliente() {
    const clienteText = $('#id_idcliente option:selected').text();
    const clienteValue = $('#id_idcliente').val();
    
    if (clienteValue && clienteValue !== '0') {
        // Assuming the value is in format "id_ruc_direccion"
        const datos = clienteValue.split('_');
        $('#ruc').val(datos[1] || '');
        $('#direccion').val(datos[2] || '');
    }
}

function mostrarProducto() {
    const productoId = $('#producto_id').val();
    if (productoId && productoId !== '0') {
        $.get(`/get_producto_info/${productoId}/`, function(data) {
            $('#unidad').val(data.unidad);
            $('#precio').val(data.precio);
            $('#stock').val(data.stock);
        });
    }
}

function mostrarTipo() {
    const tipoId = $('#id_tipo').val();
    if (tipoId) {
        $.get(`/get_tipo_info/${tipoId}/`, function(data) {
            $('#id_nrodoc').val(data.numeracion);
        });
    }
}

function mostrarMensajeError(mensaje) {
    $('#error-message').removeClass('hidden').text(mensaje);
    setTimeout(function() {
        $('#error-message').addClass('hidden');
    }, 5000);
}

function agregarDetalle() {
    const ruc = $('#ruc').val();
    if (!ruc) {
        mostrarMensajeError("Por favor seleccione el Cliente");
        return false;
    }
    
    const productoId = $('#producto_id').val();
    const productoDesc = $('#producto_id option:selected').text();
    if (productoId === '0') {
        mostrarMensajeError("Por favor seleccione el Producto");
        return false;
    }
    
    const cantidad = parseFloat($('#cantidad').val()) || 0;
    const stock = parseFloat($('#stock').val()) || 0;
    
    if (cantidad <= 0) {
        mostrarMensajeError("Por favor ingrese cantidad del producto mayor a 0");
        return false;
    }
    
    if (cantidad > stock) {
        mostrarMensajeError(`No se tiene tal cantidad de producto, solo hay ${stock}`);
        return false;
    }
    
    const precio = parseFloat($('#precio').val()) || 0;
    if (precio <= 0) {
        mostrarMensajeError("Por favor ingrese precio de venta del producto");
        return false;
    }
    
    // Check for duplicate products
    if (controlproducto.includes(productoId)) {
        mostrarMensajeError("No puede volver a vender el mismo producto");
        return false;
    }
    
    // Add to cart
    const unidad = $('#unidad').val();
    const itemSubtotal = cantidad * precio;
    
    subtotal[cont] = itemSubtotal;
    controlproducto[cont] = productoId;
    total += itemSubtotal;
    
    const fila = `
        <tr class="selected" id="fila${cont}">
            <td class="text-center">
                <button type="button" class="btn btn-danger btn-xs" onclick="eliminardetalle('${productoId}', ${cont});">
                    <i class="fas fa-times"></i>
                </button>
            </td>
            <td class="text-right">
                <input type="hidden" name="cod_producto[]" value="${productoId}">
                ${productoId}
            </td>
            <td>${productoDesc}</td>
            <td>
                <input type="hidden" name="unidad[]" value="${unidad}">
                ${unidad}
            </td>
            <td class="text-right">
                <input type="hidden" name="cantidad[]" value="${cantidad}">
                ${cantidad}
            </td>
            <td class="text-right">
                <input type="hidden" name="pventa[]" value="${precio}">
                ${precio.toFixed(2)}
            </td>
            <td class="text-right">${itemSubtotal.toFixed(2)}</td>
        </tr>
    `;
    
    $('#detalles tbody').append(fila);
    detalleventa.push({
        codigo: productoId,
        unidad: unidad,
        cantidad: cantidad,
        pventa: precio,
        subtotal: itemSubtotal
    });
    
    cont++;
    $('#total').val(total.toFixed(2));
    limpiar();
}

function limpiar() {
    $('#cantidad').val('');
    $('#precio').val('');
    $('#producto_id').val('0').trigger('change');
}

function eliminardetalle(codigo, index) {
    total -= subtotal[index];
    $('#fila' + index).remove();
    
    const pos = controlproducto.indexOf(codigo);
    if (pos !== -1) {
        controlproducto.splice(pos, 1);
        detalleventa.splice(pos, 1);
    }
    
    $('#total').val(total.toFixed(2));
}