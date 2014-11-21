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


jQuery(document).ready(function(){
   jQuery('#billing_street').show();
   jQuery('#billing_city').show();
   jQuery('#billing_postcode').show();
   jQuery('#billing_country').show();
   jQuery('#billing_checkbox').change(function(){
        if(jQuery('#billing_checkbox').prop('checked')) {
            jQuery('#billing_street').hide();
            jQuery('#billing_city').hide();
            jQuery('#billing_postcode').hide();
            jQuery('#billing_country').hide();
        }
        else{
            jQuery('#billing_street').show();
            jQuery('#billing_city').show();
            jQuery('#billing_postcode').show();
            jQuery('#billing_country').show();

        }
       });
});