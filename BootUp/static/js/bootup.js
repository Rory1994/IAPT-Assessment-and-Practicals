//
//function toggleAddressAvailibility()
//{
//if (document.getElementById('billing_checkbox').checked == false)
//  {
//  document.getElementById('billing_street').show();
//  document.getElementById('billing_city').show();
//  document.getElementById('billing_postcode').show();
//  document.getElementById('billing_country').show();
//  }
//else
//  {
//  document.getElementById('billing_street').hide();
//  document.getElementById('billing_city').hide();
//  document.getElementById('billing_postcode').hide();
//  document.getElementById('billing_country').hide();
//  }
//}


$(document).ready(function(){

   var pledge_count = 6;
   $('#billing_street').show();
   $('#billing_city').show();
   $('#billing_postcode').show();
   $('#billing_country').show();
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
   //$('#add_pledge').onclick(function(){
     //  <input id='pledgeValue' name='pledge' type='text' /> <

  // });


});