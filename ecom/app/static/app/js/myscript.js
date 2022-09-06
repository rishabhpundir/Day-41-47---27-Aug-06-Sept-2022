$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]

    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            product_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2]

    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            product_id:id
        },
        success: function(data){
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
        }
    })
})

$('.remove-item').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this

    $.ajax({
        type: "GET",
        url: "/removeitem",
        data: {
            product_id:id
        },
        success: function(data){
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total_amount").innerText = data.total_amount
            document.getElementById("total_items").innerText = data.total_items
            eml.parentNode.parentNode.parentNode.parentNode.remove()
        }
    })
})