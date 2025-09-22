$("#usernameId").on("input", () => {
    const largoTexto = $("#usernameId").val().length;
    const parrafo = $("#pUsernameid");
    const inputUsername = $("#usernameId");
  
    if (largoTexto <= 2 || largoTexto >= 15) {
      inputUsername.removeClass("is-valid").addClass("is-invalid");
      parrafo
        .text("El nombre de usuario debe contener entre 3 y 15 caracteres")
        .css({ color: "red", fontSize: "14px" });
    } else {
      inputUsername.removeClass("is-invalid").addClass("is-valid");
      parrafo.text("").css({ color: "", fontSize: "" });
    }
  });
  
  $("#nameId").on("input", () => {
    const largoTexto = $("#nameId").val().length;
    const parrafo = $("#pNameid");
    const inputName = $("#nameId");
  
    if (largoTexto <= 3 || largoTexto >= 15) {
      inputName.removeClass("is-valid").addClass("is-invalid");
      parrafo
        .text("El nombre de usuario debe contener entre 3 y 15 caracteres")
        .css({ color: "red", fontSize: "14px" });
    } else {
      inputName.removeClass("is-invalid").addClass("is-valid");
      parrafo.text("").css({ color: "", fontSize: "" });
    }
  });
  
  $("#lastNameId").on("input", () => {
    const largoTexto = $("#lastNameId").val().length;
    const parrafo = $("#pLastnameid");
    const inputLastname = $("#lastNameId");
  
    if (largoTexto <= 3 || largoTexto >= 15) {
      inputLastname.removeClass("is-valid").addClass("is-invalid");
      parrafo
        .text("El nombre de usuario debe contener entre 3 y 15 caracteres")
        .css({ color: "red", fontSize: "14px" });
    } else {
      inputLastname.removeClass("is-invalid").addClass("is-valid");
      parrafo.text("").css({ color: "", fontSize: "" });
    }
  });
  
  $("#emailId2").on("input", () => {
    const email1 = $("#emailId").val();
    const email2 = $("#emailId2").val();
    const parrafo = $("#pEmailid");
  
    if (email1 !== email2) {
      $("#emailId, #emailId2").addClass("is-invalid");
      $("#emailId, #emailId2").removeClass("is-valid");
      parrafo.text("Los correos no coinciden");
      parrafo.css({ color: "red", fontSize: "14px" });
    } else {
      $("#emailId, #emailId2").removeClass("is-invalid");
      $("#emailId, #emailId2").addClass("is-valid");
      parrafo.text("");
    }
  });
  
  $("#passwordId2").on("input", () => {
    const pass1 = $("#passwordId").val();
    const pass2 = $("#passwordId2").val();
    const parrafo = $("#pPasswordid");
  
    if (pass1 !== pass2) {
      $("#passwordId, #passwordId2").addClass("is-invalid");
      $("#passwordId, #passwordId2").removeClass("is-valid");
      parrafo.text("Las contraseñas no coinciden");
      parrafo.css({ color: "red", fontSize: "14px" });
    } else {
      $("#passwordId, #passwordId2").removeClass("is-invalid");
      $("#passwordId, #passwordId2").addClass("is-valid");
      parrafo.text("");
    }
  });
  
  $("#btn-minus").click(() => {
    const valorActual = parseInt($("#cantidadId").val());
    if (valorActual >= 1) {
      $('#cantidadId').val(valorActual - 1);
    }
  });

  $("#btn-plus").click(() => {
    const valorActual = parseInt($("#cantidadId").val());
    if (valorActual >= 0) {
      $('#cantidadId').val(valorActual + 1);
    }
  });

// // Captura el evento clic en el botón "Agregar al Carrito"
// document.querySelectorAll('.agregar-carrito').forEach(button => {
//   button.addEventListener('click', function() {
//       const productoId = this.getAttribute('data-producto-id');
//       addProducttoCart(productoId);
//       console.log('si paso')
//   });
// });

// funcion para pasar los datos del boton al carrito
$('.col-md-4').on('click', '.agregar-carrito', function() {
  // Obtener el valor del producto ID del botón clickeado
  var productoId = $(this).val();
  // Llamar a la función para agregar el producto al carrito
  addProducttoCart(productoId);
});

// $('.card').on('click', '.agregar-carrito', function() {
//   // Obtener el valor del producto ID del botón clickeado
//   var productoId = $(this).val();
//   console.log('Producto ID:', productoId);
//   console.log(csrftoken)
//   // Llamar a la función para agregar el producto al carrito
//   addProducttoCart(productoId);
// });

function addProducttoCart(productoId) {
  // Envía una solicitud AJAX para agregar el producto al carrito
  $.ajax({
    url: `http://127.0.0.1:8000/cart/add/`,
    type: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'), // Incluye el token CSRF
    },
    data: {
      productoId: productoId,
      csrfmiddlewaretoken: getCookie('csrftoken'), // Asegúrate de que el nombre del token CSRF sea correcto
      action: 'post'},
      success: function(json){
              document.getElementById('cart_quantity').
              textContent = json.qty
      },  

      error: function(xhr, status, error) {
       console.error('Error al agregar producto al carrito:', error);
     }
   });
 };


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

//actualizar cantidad de producto en el carro de compras 
 $('.col-md-9').on('click', '.update-cart', function() {
   // Obtener el valor del producto ID del botón clickeado
   var productoId = $(this).data('index');
   // Llamar a la función para agregar el producto al carrito
   updateProductCart(productoId);
 });

 function updateProductCart(productoId) {
  // Envía una solicitud AJAX para agregar el producto al carrito
  $.ajax({
    url: `http://127.0.0.1:8000/cart/update/`,
    type: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'), // Incluye el token CSRF
    },
    data: {
      productoId: productoId,
      product_qty: $('#select' + productoId + ' option:selected').text(),
      csrfmiddlewaretoken: getCookie('csrftoken'), // Asegúrate de que el nombre del token CSRF sea correcto
      action: 'post'},
      success: function(json){
              // document.getElementById('cart_quantity').
              // textContent = json.qty
              location.reload();

      },  

      error: function(xhr, status, error) {
      console.error('Error al actualizar el producto al carrito:', error);
     }
   });
 };

//borra un producto del carro de compras 
$('.col-md-9').on('click', '.delete-cart', function() {
  var productoId = $(this).data('index');
  deleteProductCart(productoId);
});

function deleteProductCart(productoId) {
 // Envía una solicitud AJAX para agregar el producto al carrito
 $.ajax({
   url: `http://127.0.0.1:8000/cart/delete/`,
   type: 'POST',
   headers: {
     'X-CSRFToken': getCookie('csrftoken'), // Incluye el token CSRF
   },
   data: {
     productoId: productoId,
     csrfmiddlewaretoken: getCookie('csrftoken'), // Asegúrate de que el nombre del token CSRF sea correcto
     action: 'post'},
     success: function(json){
      location.reload();
     },  

     error: function(xhr, status, error) {
     console.error('Error al actualizar el producto al carrito:', error);
    }
  });
};

function confirmDelete(productoId) {
  Swal.fire({
      title: '¿Estás seguro?',
      text: "¡No podrás revertir esto!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminarlo'
  }).then((result) => {
      if (result.isConfirmed) {
          window.location.href = "/eliminar_producto/"+productoId;
      }
  });
}

function confirmDeleteMultiple() {
  Swal.fire({
      title: '¿Eliminar productos seleccionados?',
      text: "Esta acción no se puede deshacer.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar'
  }).then((result) => {
      if (result.isConfirmed) {
          document.forms[0].submit();  // Enviar el formulario
      }
  });
}

function confirmCategoria() {
  Swal.fire({
      title: '¿Eliminar categoria seleccionada?',
      text: "Esta acción no se puede deshacer.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar'
  }).then((result) => {
      if (result.isConfirmed) {
          document.forms[2].submit();  // Enviar el formulario
      }
  });
}


$("#precioId").on("input", () => {
  const precio = $("#precioId").val();
  const parrafo = $("#pPrecioId");

  if (precio < 0 ) {
    $("#precioId").addClass("is-invalid");
    $("#precioId").removeClass("is-valid");
    parrafo.text("El valor no puede ser menor a 0");
    parrafo.css({ color: "red", fontSize: "14px" });
  } else {
    $("#emailId").removeClass("is-invalid");
    $("#emailId").addClass("is-valid");
    parrafo.text("");
  }
});

$("#cantidadId").on("input", () => {
  const cantidad = $("#cantidadId").val();
  const parrafo = $("#pCantidadId");

  if (cantidad < 0 ) {
    $("#cantidadId").addClass("is-invalid");
    $("#cantidadId").removeClass("is-valid");
    parrafo.text("El valor no puede ser menor a 0");
    parrafo.css({ color: "red", fontSize: "14px" });
  } else {
    $("#cantidadId").removeClass("is-invalid");
    $("#cantidadId").addClass("is-valid");
    parrafo.text("");
  }
});