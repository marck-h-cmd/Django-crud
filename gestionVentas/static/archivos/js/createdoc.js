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
            
            // 👈 NUEVO: Mostrar información del stock
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
    
    stockCantidad.removeClass('stock-disponible stock-medio stock-bajo');
    stockWarning.hide();
    
    if (stock <= 0) {
        stockCantidad.addClass('stock-bajo');
        stockMessage.text('⚠️ Producto sin stock disponible');
        stockWarning.show();
    } else if (stock <= 5) {
        stockCantidad.addClass('stock-bajo');
        stockMessage.text('⚠️ Stock bajo - Quedan pocas unidades');
        stockWarning.show();
    } else if (stock <= 20) {
        stockCantidad.addClass('stock-medio');
        stockMessage.text('⚠️ Stock medio - Considere reabastecer pronto');
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
                <button type="button" class="btn btn-danger btn-xs" onclick="eliminardetalle('${idproducto}', ${cont});">
                    <i class="fas fa-times"></i>
                </button>
            </td>
            <td class="text-right">
                <input type="hidden" name="cod_producto[]" value="${idproducto}">
                ${idproducto}
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
        codigo: idproducto,
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
    $('#idproducto').val('0').trigger('change');
    $('#stock-display').hide();
    $('#cantidad').removeClass('is-invalid').tooltip('hide');
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