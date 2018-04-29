function joinGroup(){
    $("#joinSuccess").html("<h5>you want to join the group, but i dont know how</h5>");
}

function createGroupPage(){
    var item = document.getElementById("createGroupFormdiv");
    item.className = 'unhidden';

    var join = document.getElementById("joinGroupDiv");
    join.className = 'hidden';

    $("#groupTable").html("");

    // $("#joinSuccess").html(`<form id="createGroupForm">`+form+`</form>`);
}

function createAGroup(){
      console.log("looking to create a group")
      $.ajax({
          url: '/createGroup',
          data: $('#createGroupForm').serialize(),
          type: 'POST',
          success: function(response) {
              console.log(response);
          },
          error: function(error) {
              console.log(error);
          }
      });
    };

$(function() {
    $('#searchGroup').click(function() {
        $.ajax({
            url: '/searchGroup',
            data: $('#groupForm').serialize(),
            type: 'POST',
            success: function(response) {
                $("#joinSuccess").html("");
                $("#createGroupForm").html("");
                console.log(response);
                list = JSON.parse(response);
                console.log(list.result)
                if (list.result == 0){
                    $("#groupTable").html("Please <a href=showSignUp>sign in</a> first.");
                } else if (list.result == -1) {
                    $("#groupTable").html("<h3>No group with that ID was found.</h3>");
                } else {
                    var data = "";
                    for (var i = 0; i<list.Passengers.length; i++) {
                      id = list.Passengers[i][0];
                      age  = list.Passengers[i][1];
                      gender = list.Passengers[i][2];
                      name = list.Passengers[i][3];
                      data += ("<tr><td>"+id+"</td><td>"+name+"</td><td>"+age+"</td><td>"+gender+"</td></tr>");
                      console.log(data);
                    }
                    var result = '<table class="table"><thead><tr><th scope="col">#</th><th scope="col">Name</th><th scope="col">Age</th><th scope="col">Gender</th></tr></thead><tbody>'+data+'</tbody></table>';
                    var item = document.getElementById("joinGroupDiv");
                    item.className = 'unhidden';
                    $("#groupTable").html(result);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
