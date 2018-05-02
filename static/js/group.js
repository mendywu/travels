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

    item = document.getElementById("joinError");
    item.className = 'hidden';

    $("#groupTable").html("");
    $('#plan').html("");
    $('#cost').html("");
    $('#totalcost').html("");
    $('#groupInfo').html("");
    $('#groupSelected').html("");
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
          } else if (resp.message == 0) {
            var item = document.getElementById("sizeError");
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

function selectGroup() {
  $.ajax({
      url: '/selectGroup',
      data: $('#groupForm').serialize(),
      type: 'POST',
      success: function(response) {
          $('#groupSelected').html("<h4>Group selected.</h4>");
          console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function createAGroup(){
      $('#plan').html("");
      $('#cost').html("");
      $('#groupSelected').html("");
      $('#groupInfo').html("");
      $('#totalcost').html("");
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
              } else if (response.message == 0) {
                  console.log("you're not logged in")
                  var item = document.getElementById("logInError");
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
        $('#plan').html("");
        $('#cost').html("");
        $('#groupInfo').html("");
        $('#totalcost').html("");
        $('#groupSelected').html("");
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
                      fname = list.Passengers[i][4];
                      lname = list.Passengers[i][5];
                      data += ("<tr><td>"+id+"</td><td>"+fname+"</td><td>"+lname+"</td><td>"+age+"</td><td>"+gender+"</td></tr>");
                      console.log(data);
                    }
                    var result = '<table class="table"><thead><tr><th scope="col">#</th><th scope="col">First Name</th><th scope="col">Last Name</th><th scope="col">Age</th><th scope="col">Gender</th></tr></thead><tbody>'+data+'</tbody></table>';
                    $('#groupInfo').html("<h5>Group ID:  "+list.GrpID+" Size:  "+list.Passengers.length+" / "+list.GrpSize+"</h5>");
                    $("#groupTable").html(result);
                    if (list.Transport != 0) {
                      if (list.Date == 0){
                        $('#plan').html("<h5>Traveling from "+list.Location[0]+" to "+list.Location[1]+" by "+list.Transport+"</h5>");
                      } else {
                        $('#plan').html("<h5>Traveling from "+list.Location[0]+" to "+list.Location[1]+" by "+list.Transport+" on "+list.Date+"</h5>");
                      }
                      if (list.Accom != "None"){
                        $('#plan').append("<h5>Staying at "+list.Accom+"</h5>")
                      }
                      $('#cost').html("<h5>Cost of trip per person: $"+list.Cost+"</h5>");
                      $('#totalcost').html("<h5>Total Cost: $"+(list.Cost*list.Passengers.length)+"</h5>");
                    } else {
                      $('#plan').html("<h5>No travel plans yet.</h5>");
                    }
                    var item = document.getElementById("joinGroupDiv");
                    item.className = 'unhidden';
                    if (list.inGroup == 1) { // current user is in the group
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

$('#groupForm').submit(function () {
     searching();
     return false;
    });
$('#createGroupForm').submit(function () {
    createAGroup();
    return false;
});
