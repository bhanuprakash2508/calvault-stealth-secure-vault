let timeout;

/* RESET TIMER */

function resetTimer(){

    clearTimeout(timeout);

    timeout = setTimeout(

        lockVault,
        300000      // 5 minutes
    );
}

/* LOCK VAULT */

function lockVault(){

    window.location.href =
        "/lock-vault";
}

/* USER ACTIVITY */

document.addEventListener(

    "mousemove",
    resetTimer
);

document.addEventListener(

    "keypress",
    resetTimer
);

document.addEventListener(

    "click",
    resetTimer
);

/* START TIMER */

resetTimer();