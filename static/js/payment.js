$(function() {
    $('#searchPaymentOptions').click(function() {
        $.ajax({
            url: '/viewPaymentOptions',
            type: 'POST',
            success: function(response) {
                console.log(response);
                list = JSON.parse(response);
                var label = "";
                label += "<h1>Current Saved Payment Options: </h1>";
                $("#sd").html(label);
                console.log(list.curID);
                var data = "";
                for (var i = 0; i<list.options.length; i++) {
                  cardNumber = list.options[i][0];
                  cardType  = list.options[i][1];
                  data += ("<tr><td>"+cardNumber+"</td><td>"+cardType+"</td><tr>");
                  console.log(data);
                }
                var result = '<table class="table"><thead><tr><th scope="col">Card Number</th><th scope="col">Card Type</th><tbody>'+data+'</tbody></table>';
                console.log(result);
                $("#PaymentOptions").html(result);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $('#addPaymentOptions').click(function() {
        $.ajax({
            url: '/addPaymentOptions',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                list = JSON.parse(response);
                var label = "";
                label += "<h1>Current Saved Payment Options: </h1>";
                $("#sd").html(label);
                console.log(list.curID);
                var data = "";
                for (var i = 0; i<list.options.length; i++) {
                  cardNumber = list.options[i][0];
                  cardType  = list.options[i][1];
                  data += ("<tr><td>"+cardNumber+"</td><td>"+cardType+"</td><tr>");
                  console.log(data);
                }
                var result = '<table class="table"><thead><tr><th scope="col">Card Number</th><th scope="col">Card Type</th><tbody>'+data+'</tbody></table>';
                console.log(result);
                $("#PaymentOptions").html(result);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $('#choosePaymentMethod').click(function() {
        $.ajax({
            url: '/choosePaymentMethod',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                list = JSON.parse(response);
                if (list.response == 'ok'){
                  $("#paymentMethodConfirmation").html("<h2>Selection Confirmed</h2>");
                }
                else{
                  $("#paymentMethodConfirmation").html("<h2>Invalid Selection</h2>");
                }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
