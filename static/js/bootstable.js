//this function working for the checking box.when checking box is checked, the rowid and checked status will be sent to falsk.
function rowCheck(box) {
    //this is a founction that if rownocheck button is clicked, then change the icon from nocheck to check.
    var $row = $(box).parents('tr');
    var $row_id=$(box).attr('id');


    var $checking=box.checked
    var result=$row_id+";"+$checking
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "edit");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhttp.send(result);

    }





function rowAcep(but) {
    $(but).parent().find('#bAcep').show();
    var $row = $(but).parents('tr');
    var $cols = $row.find('td');
    var $row = $(but).parents('tr');
    var $row_value=$row.text()
    var $row_id=$(but).attr("name")
    var comment=$row_id+";"+$row_value
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "comment");
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhttp.send(comment);
    alert("Your comment is saved!");


}

async function searchAcep(but) {

    $(but).parent().find('#bAcep').show();
    var $row = $(but).parents('tr');
    var $cols = $row.find('td');
    var $row = $(but).parents('tr');
    var $row_id=$(but).attr("name")
//    let data={"id":$row_id}
//
//    let res=await fetch("knowledge",{method:'POST',headers:{'Content-Type':'application/json',},body:JSON.stringify(data)})
//    return res

    let windowName = 'w_' + Date.now() + Math.floor(Math.random() * 100000).toString();
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "knowledge");

    form.setAttribute("target", windowName);

    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "message");
    hiddenField.setAttribute("value", $row_id);
    form.appendChild(hiddenField);
    document.body.appendChild(form);

    window.open('', windowName);

    form.submit();


//
//    const xhttp = new XMLHttpRequest();
//    xhttp.open("POST", "knowledge");
//    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
//    xhttp.send($row_id);



}

