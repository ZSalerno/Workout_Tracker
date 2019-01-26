
<!--Get html from the last row of table and append it in a new row. Not taking values of inputs-->
function addRow() {
    var html = $('#exTable tr:last').html();
    $('#exTable tr:last').after("<tr>" + html + "</tr>");
    $('#exTable tr:last').find('textarea,input,select').prop('disabled', false);
}

function deleteRow(r) {
  var i = r.parentNode.parentNode.parentNode.rowIndex;
  document.getElementById("exTable").deleteRow(i);
}

<!--Check if a string, target, contains any strings in the list, pattern-->
function contains(target, pattern){
    var value = 0;
    pattern.forEach(function(word){
      value = value + target.includes(word);
    });
    return (value === 1)
}

<!--Return a copied row directly beneath the row where copy button was selected-->
function copyRow(r){
    <!--Get ID of the row selected-->
    var i = r.parentNode.parentNode.parentNode.rowIndex;

    <!--WORKING SECTION - COMMENTED OUT TO TRY CLONE METHOD-->
    <!--Get HTML of the last row in table.-->
    <!--Should be HTML of row selected-->
    <!--var html = $('#exTable tr:last').html();-->

    <!--Add new row in index after row selected-->
    <!--$('#exTable > tbody > tr').eq(i-1).after("<tr>" + html + "</tr>");-->
    <!--END WORKING COMMENT OUT-->

    <!--Clone row where button was clicked and add below. Doesn't work for SELECTS-->
    var cloneRow = $('#exTable > tbody > tr').eq(i-1).clone()
    $('#exTable > tbody > tr').eq(i-1).after(cloneRow);

    <!--Copy Select value for new row because it is lost when using .clone() above-->
    <!--Get newRow variable to replace IDs later-->
    var newRow = $('#exTable > tbody > tr').eq(i)
    var originalSelect = $('#exTable > tbody > tr').eq(i-1).find('select option:selected').val();
    newRow.find('select').val(originalSelect);

    <!--List ids will be used for disable loop. newId is new id of element. words are elements that should be disabled-->
    var ids = [];
    var newId = '';
    var oldId = '';
    var words = ["lift", "date", "comments"];

    <!--Append the index of the row to the ID of each element within it-->
    $(newRow).find("[id]").add(newRow).each(function() {
        <!--Remove numbers from current ID value-->
        newId = this.id.replace(/[0-9]/g, '') + i.toString();
        oldId = this.id
        this.id = newId


        <!--Check if current ID belongs to the list of elements that should be disabled-->
        nameCheck = contains(newId, words);
        if (nameCheck) {
            ids.push('#'+newId)
        }
    })

    <!--Loop through list of IDs of elements to be disabled and disable them-->
    var i;
    for (i = 0; i < ids.length; i++) {
        $(ids[i]).prop("disabled", true);
    }
}


<!--$("#exForm").submit(function(){-->
    <!--alert("Hi");-->
    <!--var data = $(this).serialize()-->
    <!--alert(data)-->
    <!--preventDefault();-->
    <!--dataString.login = $("#login").val();-->
    <!--dataString.password = $("#password").val();-->
    <!--$.ajax({-->
    <!--type: 'POST',-->
    <!--url: 'http://localhost:8080/login',-->
    <!--data: JSON.stringify(dataString),-->
      <!--contentType: 'application/json',-->
    <!--dataType: 'json',-->
    <!--success: function(response) {-->
        <!--console.log(response);-->
    <!--},-->
    <!--error: function(response) {-->
            <!--console.log(response);-->
    <!--}-->
  <!--});-->
<!--});-->

function saveRow(r){
    <!--Get ID of the row selected-->
    var i = r.parentNode.parentNode.parentNode.rowIndex;

    <!--Create row variable to use throughout function-->
    var rowToSave = $('#exTable > tbody > tr').eq(i-1)

    <!--Commented out in case i figure out how to make this a loop instead of copy paste-->
    <!--fields = ["date", "lift", "weight", "sets", "reps", "comments"]-->

    <!--Get all row data-->
    var date = rowToSave.find("[name=date]").val();
    var lift = rowToSave.find("[name=lift]").val();
    var weight = rowToSave.find("[name=weight]").val();
    var sets = rowToSave.find("[name=sets]").val();
    var reps = rowToSave.find("[name=reps]").val();
    var comments = rowToSave.find("[name=comments]").val();

    if (weight == '' || sets == '' || reps == ''){
        alert("Weight, Sets and Reps must have values");
        return;
    }

    <!--Create json object and convert it to string-->
    rowJson ={ "date":date, "lift":lift, "weight":weight, "sets":sets, "reps":reps, "comments":comments }

    $.ajax({
        url: '/saveExercise',
        data: rowJson,
        success: function(response){
            console.log(response);
            rowToSave.animate({
                backgroundColor: "#b3ffb3",
            }, 500 );
        },
        error: function(error){
            console.log(error);
            rowToSave.animate({
                backgroundColor: "#ff8080",
            }, 500 );
        }
    });
};