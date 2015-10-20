 
var adblock = false;

function adBlockDetected() {
    adblock = true;
}

function adBlockNotDetected() {
    adblock = false;
}

 if(typeof fuckAdBlock === 'undefined') {
    adBlockDetected();
} else {
    fuckAdBlock.onDetected(adBlockDetected);
    fuckAdBlock.onNotDetected(adBlockNotDetected);
    // and|or
    fuckAdBlock.on(true, adBlockDetected);
    fuckAdBlock.on(false, adBlockNotDetected);
    // and|or
    fuckAdBlock.on(true, adBlockDetected).onNotDetected(adBlockNotDetected);
}


 if (adblock){
   $('#_carbonads_js').after('<span class="ab-msg">I rely on ad-revenue to cover server costs. please consider disabling adblocker or <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=FRUJ7J8X43DWN&lc=IL&item_name=LibreStock&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donate_LG%2egif%3aNonHosted">donating</a> - you will see only one small ad per page, promise :)</span>');
 }