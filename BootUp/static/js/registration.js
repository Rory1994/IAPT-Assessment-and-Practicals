/**
 * Created by rs1019 on 18/11/14.
 */

function toggleAddressAvailibility()
{
if (document.getElementById('billing_checkbox').checked == false)
  {
  document.getElementById('billing_street').removeAttribute('disabled');
  document.getElementById('billing_city').removeAttribute('disabled');
  document.getElementById('billing_postcode').removeAttribute('disabled');
  document.getElementById('billing_country').removeAttribute('disabled');
  }
else
  {
  document.getElementById('billing_street').setAttribute('disabled','disabled');
  document.getElementById('billing_city').setAttribute('disabled','disabled');
  document.getElementById('billing_postcode').setAttribute('disabled','disabled');
  document.getElementById('billing_country').setAttribute('disabled','disabled');
  }
}
