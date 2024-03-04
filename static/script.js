$(document).ready(function(){
    $("#cities").change(function(){
        var selectedCity = $(this).val();
        if(selectedCity == "warsaw") {
            $("#name1").val("Warszawa");
            $("#Latitude1").val("52.2297");
            $("#Longitude1").val("21.0122");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if(selectedCity == "berlin") {
            $("#name1").val("Berlin");
            $("#Latitude1").val("52.5200");
            $("#Longitude1").val("13.4050");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        } else if(selectedCity == "losangeles") {
            $("#name1").val("Los Angeles");
            $("#Latitude1").val("34.0522");
            $("#Longitude1").val("118.2436");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-west']").prop("checked", true);
        } else if(selectedCity == "bangkok") {
            $("#name1").val("Bangkok");
            $("#Latitude1").val("13.7539");
            $("#Longitude1").val("100.5014");
            $("input[name='start-v'][value='dot-start-north']").prop("checked", true);
            $("input[name='start-h'][value='dot-start-east']").prop("checked", true);
        }
    });
});

$(document).ready(function(){
    $("#cities2").change(function(){
        var selectedCity = $(this).val();
        if(selectedCity == "warsaw") {
            $("#name2").val("Warszawa");
            $("#Latitude2").val("52.2297");
            $("#Longitude2").val("21.0122");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if(selectedCity == "berlin") {
            $("#name2").val("Berlin");
            $("#Latitude2").val("52.5200");
            $("#Longitude2").val("13.4050");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        } else if(selectedCity == "losangeles"){
            $("#name2").val("Los Angeles");
            $("#Latitude2").val("34.0522");
            $("#Longitude2").val("118.2436");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-west']").prop("checked", true);
        } else if(selectedCity == "bangkok") {
            $("#name2").val("Bangkok");
            $("#Latitude2").val("13.7539");
            $("#Longitude2").val("100.5014");
            $("input[name='end-v'][value='dot-end-north']").prop("checked", true);
            $("input[name='end-h'][value='dot-end-east']").prop("checked", true);
        }
    });
});