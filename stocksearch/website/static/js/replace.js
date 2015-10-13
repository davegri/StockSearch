 
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
   $('.download').replaceWith('<span class="button">Please disable Adblock on librestock.com to download photos. You will see only one sexy ad by Carbon Ads.</span>');
 }