 
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
   $('.download').replaceWith('<span class="button">I rely on ad-revenue to cover server costs. please disable adblocker to download photos - you will see only one ad per page. promise :)</span>');
 }