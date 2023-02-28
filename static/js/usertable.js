function rowCheckuser(box) {
    //this is a founction that if rownocheck button is clicked, then change the icon from nocheck to check.
    var $row = $(box).parents('tr');
    var $row_id=$(box).attr('id');


    var $checking=box.checked
    var result=$row_id+";"+$checking
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "status");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhttp.send(result);

    }