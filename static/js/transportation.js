$(function() {
    $('#searchTransportation').click(function() {
        $.ajax({
            url: '/searchTransportation',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                list = JSON.parse(response);
                var label = "";
                label += "<h1>Travel options from " + list.source + " to " + list.dest + " on " + list.departDate + "</h1>";
                $("#sd").html(label);

                var rlabel = "";
                rlabel += "<h1>Travel options from " + list.dest + " to " + list.source + " on " + list.returnDate + "</h1>";
                $("#rsd").html(rlabel);

                var data = "";
                for (var i = 0; i<list.departOptions.length; i++) {
                  id = list.departOptions[i][0];
                  cost  = list.departOptions[i][1];
                  carrier = list.departOptions[i][2];
                  klass = list.departOptions[i][3];
                  data += ("<tr><td>"+id+"</td><td>$"+cost+"</td><td>"+carrier+"</td><td>"+klass+"</td><tr>");
                  console.log(data);
                }
                var result = '<table class="table"><thead><tr><th scope="col">ID</th><th scope="col">Cost</th><th scope="col">Carrier</th><th scope="col">Class</th><tbody>'+data+'</tbody></table>';
                console.log(result);
                $("#TransportOptions").html(result);

                var rdata = "";
                for (var i = 0; i<list.returnOptions.length; i++) {
                  id = list.returnOptions[i][0];
                  cost  = list.returnOptions[i][1];
                  carrier = list.returnOptions[i][2];
                  klass = list.returnOptions[i][3];
                  rdata += ("<tr><td>"+id+"</td><td>$"+cost+"</td><td>"+carrier+"</td><td>"+klass+"</td><tr>");
                  console.log(rdata);
                }
                var rresult = '<table class="table"><thead><tr><th scope="col">ID</th><th scope="col">Cost</th><th scope="col">Carrier</th><th scope="col">Class</th><tbody>'+rdata+'</tbody></table>';
                console.log(rresult);
                $("#rTransportOptions").html(rresult);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $('#chooseFlight').click(function() {
        $.ajax({
            url: '/chooseFlight',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                list = JSON.parse(response);
                if (list.response == 'ok'){
                  $("#flightConfirmation").html("<h2>Selection Confirmed</h2>");
                }
                else{
                  $("#flightConfirmation").html("<h2>Invalid Selection</h2>");
                }

            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
