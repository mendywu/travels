function createGroupPage(){
    var item = document.getElementById("createGroupFormdiv");
    item.className = 'unhidden';

    item = document.getElementById("joinGroupDiv");
    item.className = 'hidden';

    item = document.getElementById("leaveGroupDiv");
    item.className = 'hidden';

    item = document.getElementById("groupError");
    item.className = 'hidden';

    item = document.getElementById("groupSuccess");
    item.className = 'hidden';

    var joining = document.getElementById("joinError");
    joining.className = 'hidden';

    $("#groupTable").html("");
}

function joinGroup() {
  $.ajax({
      url: '/joinGroupOfficially',
      data: $('#groupForm').serialize(),
      type: 'POST',
      success: function(response) {
          resp = JSON.parse(response);
          if (resp.message == -1) {
              console.log("you already in!");
              var item = document.getElementById("joinError");
              item.className = 'unhidden';
          } else {
            searching();
          }
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function leaveGroup() {
  $.ajax({
      url: '/leaveGroup',
      data: $('#groupForm').serialize(),
      type: 'POST',
      success: function(response) {
          console.log(response);
          searching();
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function createAGroup(){
      var joining = document.getElementById("groupSuccess");
      joining.className = 'hidden';
      joining = document.getElementById("groupError");
      joining.className = 'hidden';
      joining = document.getElementById("joinError");
      joining.className = 'hidden';
      console.log("looking to create a group")
      $.ajax({
          url: '/createGroup',
          data: $('#createGroupForm').serialize(),
          type: 'POST',
          success: function(response) {
              resp = JSON.parse(response);
              if (resp.message == -1) {
                  console.log("already exists");
                  var item = document.getElementById("groupError");
                  item.className = 'unhidden';
              } else {
                document.getElementById("grpID").value =   document.getElementById("inputGrpID").value;
                searching();
              }
          },
          error: function(error) {
              console.log(error);
          }
      });
    };

function searching() {
        var item = document.getElementById("createGroupFormdiv");
        item.className = 'hidden';
        item = document.getElementById("joinGroupDiv");
        item.className = 'hidden';
        item = document.getElementById("leaveGroupDiv");
        item.className = 'hidden';
        item = document.getElementById("joinError");
        item.className = 'hidden';
        item = document.getElementById("groupSuccess");
        item.className = 'hidden';

        $.ajax({
            url: '/searchGroup',
            data: $('#groupForm').serialize(),
            type: 'POST',
            success: function(response) {
                $("#joinSuccess").html("");
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
                    $("#groupTable").html(result);
                    var item = document.getElementById("joinGroupDiv");
                    item.className = 'unhidden';
                    if (list.inGroup == 1) {
                      var item = document.getElementById("leaveGroupDiv");
                      item.className = 'unhidden';
                    }
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    };
