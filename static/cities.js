const selectBoxes = document.querySelectorAll(".selectBox")

const newRowHTML = `
<option value="bangkok">Bangkok</option>
<option value="berlin">Berlin</option>
<option value="brasilia">Brasilia</option>
<option value="lagos">Lagos</option>
<option value="losangeles">Los Angeles</option>
<option value="moskwa">Moskwa</option>
<option value="sydney">Sydney</option>
<option value="tokyo">Tokio</option>
<option value="warsaw">Warsaw</option>
`;

selectBoxes.forEach(selectBox => {
    selectBox.innerHTML += newRowHTML;
});


$(document).ready(function(){
    $("#cities").change(function(){
        var selectedCity = $(this).val();
        if (selectedCity == "warsaw") {
            $("#name1").val("Warsaw");
            $("#Latitude1").val("52.2297");
            $("#Longitude1").val("21.0122");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "berlin") {
            $("#name1").val("Berlin");
            $("#Latitude1").val("52.5200");
            $("#Longitude1").val("13.4050");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "losangeles") {
            $("#name1").val("Los Angeles");
            $("#Latitude1").val("34.0522");
            $("#Longitude1").val("118.2436");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-west']").prop("checked", true);
        } else if (selectedCity == "bangkok") {
            $("#name1").val("Bangkok");
            $("#Latitude1").val("13.7539");
            $("#Longitude1").val("100.5014");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "tokyo") {
            $("#name1").val("Tokyo");
            $("#Latitude1").val("35.6895000");
            $("#Longitude1").val("139.6917100");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "moskwa") {
            $("#name1").val("Moskwa");
            $("#Latitude1").val("55.7522200");
            $("#Longitude1").val("37.6155600");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "sydney") {
            $("#name1").val("Sydney");
            $("#Latitude1").val("33.8678500");
            $("#Longitude1").val("151.2073200");
            $("input[name='start-v'][value='dot-start-south']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "lagos") {
            $("#name1").val("Lagos");
            $("#Latitude1").val("6.4540700");
            $("#Longitude1").val("3.3946700");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if (selectedCity == "brasilia") {
            $("#name1").val("Brasilia");
            $("#Latitude1").val("15.7797200");
            $("#Longitude1").val("47.9297200");
            $("input[name='start-v'][value='dot-start-south']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-west']").prop("checked", true);
        }
    });
});

$(document).ready(function(){
    $("#cities2").change(function(){
        var selectedCity = $(this).val();
        if (selectedCity == "warsaw") {
            $("#name2").val("Warsaw");
            $("#Latitude2").val("52.2297");
            $("#Longitude2").val("21.0122");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "berlin") {
            $("#name2").val("Berlin");
            $("#Latitude2").val("52.5200");
            $("#Longitude2").val("13.4050");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "losangeles"){
            $("#name2").val("Los Angeles");
            $("#Latitude2").val("34.0522");
            $("#Longitude2").val("118.2436");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-west']").prop("checked", true);
        } else if (selectedCity == "bangkok") {
            $("#name2").val("Bangkok");
            $("#Latitude2").val("13.7539");
            $("#Longitude2").val("100.5014");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "tokyo") {
            $("#name2").val("Tokyo");
            $("#Latitude2").val("35.6895000");
            $("#Longitude2").val("139.6917100");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "moskwa") {
            $("#name2").val("Moskwa");
            $("#Latitude2").val("55.7522200");
            $("#Longitude2").val("37.6155600");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "sydney") {
            $("#name2").val("Sydney");
            $("#Latitude2").val("33.8678500");
            $("#Longitude2").val("151.2073200");
            $("input[name='end-v'][value='dot-end-south']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "lagos") {
            $("#name2").val("Lagos");
            $("#Latitude2").val("6.4540700");
            $("#Longitude2").val("3.3946700");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if (selectedCity == "brasilia") {
            $("#name2").val("Brasilia");
            $("#Latitude2").val("15.7797200");
            $("#Longitude2").val("47.9297200");
            $("input[name='end-v'][value='dot-end-south']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-west']").prop("checked", true);
        }
    });
});