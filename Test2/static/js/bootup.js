
//Exam Number: Y0071297

$(document).ready(function(){

   //var pledge_count = 6;

   $(".tip").tooltip();

   if($('#billing_checkbox').prop('checked')){
        $('#billing_street').hide();
        $('#billing_city').hide();
        $('#billing_postcode').hide();
        $('#billing_country').hide();
   }

   else{
        $('#billing_street').show();
        $('#billing_city').show();
        $('#billing_postcode').show();
        $('#billing_country').show();
   }

   $('#billing_checkbox').change(function(){
        if($('#billing_checkbox').prop('checked')) {
            $('#billing_street').hide();
            $('#billing_city').hide();
            $('#billing_postcode').hide();
            $('#billing_country').hide();
        }
        else{
            $('#billing_street').show();
            $('#billing_city').show();
            $('#billing_postcode').show();
            $('#billing_country').show();

        }
       });



});