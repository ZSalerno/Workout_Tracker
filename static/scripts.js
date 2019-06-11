//Chart theme
var themeColors = [
    "#1d1145",
    "#0db4b9",
    "#f2a1a1",
    "#e76d89",
    "#e8a668",
    "#cf5d3a",
    "#773f3f",
    "#4f7b8a",
    "#45a5aa",
];

var transparentThemeColors = [
    "#1d114566",
    "#0db4b966",
    "#f2a1a166",
    "#e76d8966",
    "#e8a66866",
    "#cf5d3a66",
    "#773f3f66",
    "#4f7b8a66",
    "#45a5aa66",
];

function getThemeColor(i) {
    return themeColors[i];
}

// Get html from the last row of table and append it in a new row. Not taking values of inputs
function addRow() {
    var html = $('#exTable tr:last').html();
    $('#exTable tr:last').after("<tr>" + html + "</tr>");
    $('#exTable tr:last').find('textarea,input,select').prop('disabled', false);
}

function deleteRow(r) {
  var i = r.parentNode.parentNode.parentNode.rowIndex;
  document.getElementById("exTable").deleteRow(i);
}

// Check if a string, target, contains any strings in the list, pattern
function contains(target, pattern){
    var value = 0;
    pattern.forEach(function(word){
      value = value + target.includes(word);
    });
    return (value === 1)
}

// Return a copied row directly beneath the row where copy button was selected
function copyRow(r){
    // Get ID of the row selected
    var i = r.parentNode.parentNode.parentNode.rowIndex;

    // Clone row where button was clicked and add below.
    var cloneRow = $('#exTable > tbody > tr').eq(i-1).clone()
    $('#exTable > tbody > tr').eq(i-1).after(cloneRow);

    // Copy Select value for new row because it is lost when using .clone() above
    // Get newRow variable to replace IDs later
    var newRow = $('#exTable > tbody > tr').eq(i)
    var originalSelect = $('#exTable > tbody > tr').eq(i-1).find('select option:selected').val();
    newRow.find('select').val(originalSelect);

    // List ids will be used for disable loop. newId is new id of element. words are elements that should be disabled
    var ids = [];
    var newId = '';
    var oldId = '';
    var words = ["lift", "date", "comments"];

    // Append the index of the row to the ID of each element within it
    $(newRow).find("[id]").add(newRow).each(function() {
        // Remove numbers from current ID value
        newId = this.id.replace(/[0-9]/g, '') + i.toString();
        oldId = this.id
        this.id = newId

        // Check if current ID belongs to the list of elements that should be disabled
        nameCheck = contains(newId.toLowerCase(), words);
        if (nameCheck) {
            ids.push('#'+newId)
        }
    })

    // Loop through list of IDs of elements to be disabled and disable them
    var i;
    for (i = 0; i < ids.length; i++) {
        $(ids[i]).prop("disabled", true);
    }
}

function saveRow(r){
    // Get ID of the row selected
    var i = r.parentNode.parentNode.parentNode.rowIndex;

    // Create row variable to use throughout function
    var rowToSave = $('#exTable > tbody > tr').eq(i-1)

    // Commented out in case i figure out how to make this a loop instead of copy paste
    // fields = ["date", "lift", "weight", "sets", "reps", "comments"]

    // Get all row data
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

    // Create json object to return to flask
    rowJson ={ "date":date, "lift":lift, "weight":weight, "sets":sets, "reps":reps, "comments":comments }

    // Send date to /saveExercise app route in flask. Color row green on save. Red on fail 
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

function getChartDataset(flaskData, fill=false, colors=false){
    var keys = Object.keys(flaskData);
    var datasetToReturn = [];
    for (var i = 0; i < Object.keys(flaskData).length; i++){
        datasetToReturn[i] = {
            label: keys[i],  //Needs to be a variable - Wrong for lifts and Month by month. Always starts at first date. Not lift or month
            fill: fill,
            data: flaskData[keys[i]],
            lineTension: 0,
        }
        if(colors){
            datasetToReturn[i].backgroundColor = themeColors[i];
            datasetToReturn[i].borderColor = themeColors[i]
        }
    }

    return datasetToReturn;
};

//TODO Need to make this the full function used in both calls in visualizations.html
function getChartDatasetTEMP (flaskData, key, fill=false, colors=false){
    var datasetToReturn = [];

    datasetToReturn[0] = {
        label: key,  //Needs to be a variable
        fill: fill,
        data: flaskData[key],
        lineTension: 0,
    }
    if(colors){
        datasetToReturn[0].backgroundColor = themeColors[i];
        datasetToReturn[i=0].borderColor = themeColors[i]
    }

    return datasetToReturn;
};