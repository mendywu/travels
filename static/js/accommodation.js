function selectAccom(){
  $.ajax({
      url: '/selectAccom',
      data: $('#selectAccommForm').serialize(),
      type: 'POST',
      success: function(response) {
          resp = JSON.parse(response);
          if (resp.message == 1) {
              var item = document.getElementById("acomSelectSuccess");
              item.className = 'unhidden';
          } else {
            var item = document.getElementById("acomSelectSuccess");
            item.className = 'hidden';
          }
      },
      error: function(error) {
          console.log(error);
      }
  });
}
