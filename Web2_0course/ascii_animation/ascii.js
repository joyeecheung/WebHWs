// 12330402, Zhang Qiuyi
// An customized animation of a Dalek shouting 'EXTERMINATE'!! >w<
var custom = 
"                        EXTERMINATE!\n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )\n" + 
"              |======|\n" + 
"              [IIIIII] -- (\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" + 
"\n" + 
"\n" + "=====\n"+
"                        \n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )\n" + 
"              |======|\n" + 
"              [IIIIII] -- (=G===\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" +  
"\n" + 
"\n" + "=====\n"+
"                        EXTERMINATE!\n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )\n" + 
"              |======|\n" + 
"              [IIIIII] -- (   =G===\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" +  
"\n" + 
"\n" + "=====\n"+
"                        \n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )\n" + 
"              |======|\n" + 
"              [IIIIII] -- (                 =G===\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" +  
"\n" + 
"\n" + "=====\n"+
"                        EXTERMINATE!\n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )\n" + 
"              |======|\n" + 
"              [IIIIII] -- (                               =G===\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" +  
"\n" + 
"\n" + "=====\n"+
"                        \n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )                                     \n" +
"              |======|                                      **\n" + 
"              [IIIIII] -- (                                  *\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" +  
"\n" + 
"\n" + "=====\n"+
"                        EXTERMINATE!\n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )                                     *   *\n" +
"              |======|                                      **\n" + 
"              [IIIIII] -- (                                 * *\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n" +  
"\n" + 
"\n" + "=====\n"+
"                        \n" + 
"                  /\n" + 
"                 /   ___\n" + 
"             '(  '.  )\n" + 
"              |======|\n" + 
"              [IIIIII] -- (\n" + 
"              |______|\n" + 
"              C OO O D\n" + 
"             C O O O  D\n" + 
"            C O  O  O  D\n" + 
"           C_O__ O___O__D\n" + 
"          [______________]\n";

ANIMATIONS["Custom"] = custom;

// add an event to trigger after loading the page
function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            oldonload();
            func();
        }
    }
}

// display next frame
function nextFrame() {
    if (currentFrame === currentLength) {
        currentFrame = 0;
    }
    frame.value = subFrames[currentFrame]; 
    currentFrame++;
}

// start playing animation
function startPlaying() {
    if (isPlaying) return;
    timer = setInterval(nextFrame, interval);
    isPlaying = true;
}

// stop playing animation
function stopPlaying() {
    if (!isPlaying) return;
    clearInterval(timer);
    isPlaying = false;
}

// change to another animation
function changeAnimation() {
    subFrame = ANIMATIONS[this.value];
    subFrames = subFrame.split("=====\n");
    frame.value = subFrames[0];
    currentLength = subFrames.length;
    currentFrame = 0;
}

// change the size of animation
function changeSize() {
    frame.className = this.value + "Font";
}

// toggle the playing speed
function toggleSpeed() {
    if(this.checked === true) {
        if (interval === 100) return;

        interval = 100;
        if (!isPlaying) return;
        clearInterval(timer);
        timer = setInterval(nextFrame, interval);
    } else {
        if (interval === 200) return;

        interval = 200;
        if (!isPlaying) return;
        clearInterval(timer);
        timer = setInterval(nextFrame, interval);
    }
}

// initialize
function init() {
    frame = document.getElementById("displayarea");

    // add handles
    document.getElementById("btnStart").onclick = startPlaying;
    document.getElementById("btnStop").onclick = stopPlaying;
    document.getElementById("selectAnimation").onchange = changeAnimation;
    document.getElementById("speed").onclick = toggleSpeed;
    var size = document.getElementsByName("size");
    for(var i = 0; i < size.length; i++) {
        size[i].onclick = changeSize;
    }

    // initialize global variables
    interval = 200;
    isPlaying = false;
    currentFrame = 0;
    AnimationString = ANIMATIONS["Blank"];
    subFrames = AnimationString.split("=====\n");
    frame.value = subFrames[currentFrame];
    currentLength = subFrames.length;
}

addLoadEvent(init);
