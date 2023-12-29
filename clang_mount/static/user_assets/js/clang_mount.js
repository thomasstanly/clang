// reset password
$(document).on('click','.verify-email',function(e){
    e.preventDefault();
    const email = $('#email-input').val();
    console.log(email);
    $.ajax({
        type: 'POST',
        url:updateCartUrl,
        data:{
        email : email,
        csrfmiddlewaretoken: csrfToken,
        action : 'POST'
        },
        success: function (data) {
            if (data.success) {
                console.log('Email found, do something...');
                Swal.fire({
                    icon: 'success',
                    title: 'OTP',
                    text: 'OPT has been successfully forwarded to the designated email',
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Email not found!',
                });
            }
        },
        error: function () {
            console.error('AJAX request failed');
        }
    })
})

// adding the quantity to the cart
$(document).on('click','.update-cart',function(e){
        e.preventDefault();
        const pId =$(this).attr('data-item');
        const qty = $('.quantity-input-'+pId).val()// const qty = parseInt($(this).val(), 10); // coverting the string to integer and 10 is the base
        const minStock = $('.quantity-input-'+pId).attr('min')
        const maxStock = parseInt($('.quantity-input-'+pId).attr('data-max'), 10);
        
        $('.max-plus[data-item="' + pId + '"]').prop('disabled', qty >= maxStock);
        $('.max-minus[data-item="' + pId + '"]').prop('disabled', qty == minStock);
        console.log(qty,minStock,maxStock)
        console.log($('.max-plus[data-item="' + pId + '"]'));

        updateTotal()
        $.ajax({
            type: 'POST',
            url:updateCartUrl,
            data:{
                item_id: pId,
                item_qty: qty,
                csrfmiddlewaretoken: csrfToken,
                action : 'POST'
            },
            success: function (data) {
                if (data.success) {
                    console.log(data.success,data.message);
                } else {
                    console.error('Error updating cart:', data.error);
                }
            },
            error: function () {
                console.error('AJAX request failed');
            }
        })
  })
  
  function showErrorAlert(message) {
    Swal.fire({
        icon: 'error',
        title: 'Error',
        text: message,
    });
}

function updateTotal() {
      let totalSubtotal = 0;
      let totalDiscount = 0;
      let totalCount = 0 ;
      const quantityInputs = document.querySelectorAll('.quantity-input');
      

      quantityInputs.forEach(function (quantityInput) {
        const qty = parseInt(quantityInput.value, 10);
        const price = parseFloat(quantityInput.closest('tr').querySelector('.product-price').value.replace('₹', ''));
        const discount = parseFloat(quantityInput.closest('tr').querySelector('.product-discount').value.replace('₹', ''));
        const item_disc = ((discount * price)/100) *qty
        const subTotal = qty * price;
        totalSubtotal += subTotal;
        totalDiscount += item_disc;
        totalCount += qty;
      });
      
      const total = totalSubtotal - totalDiscount
      $('#sub-total').text('₹ ' + totalSubtotal.toFixed(2));
      $('#discount').text('₹ ' + totalDiscount.toFixed(2));
      $('#total').text(total.toFixed(2));
      $('#cart-count').text(totalCount);
      console.log(totalCount)
    }

// adding the product to the wishlist
$(document).on('click','.wish',function(e){
    e.preventDefault();
    const p_slug = $(this).attr('data-item');
    console.log(p_slug)
    $.ajax({
        type: 'POST',
        url:updateCartUrl,
        data:{
            slug: p_slug,
            csrfmiddlewaretoken: csrfToken,
            action : 'POST'
        },
        success: function (data) {

            if (data.success) {
                $('#wish-count').text(data.wishlist_count);
                console.log(data.wishlist_count)
            } else {
                Swal.fire({
                    icon: 'warning',
                    text: data.error,
                });
            }

        },
        error: function () {
            console.error('AJAX request failed');
        }
    })

})

$(document).on('click','.radio-button',function(e){
    e.preventDefault();
    const a_Id = $(this).attr('data-id');
    console.log(a_Id)
     $('.address-radio').removeClass('selected');

    $(this).closest('.border').find('.address-radio').addClass('selected');
    $.ajax({
        type: 'POST',
        url: updateCartUrl, 
        data: {
            address: a_Id,
            csrfmiddlewaretoken: csrfToken,
            action : 'POST' 
        },
        success: function (data) {
            if (data.success) {
                console.log(data.success) 
            } else {
               console.error('not success')
            }

        },
        error: function () {
            // Handle error
            console.error('AJAX request failed');
        }
    });
});
