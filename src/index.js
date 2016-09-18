window.AudioContext = window.AudioContext || window.webkitAudioContext;
context = new AudioContext();

var ticker = $('#slider').slider({
    step: 0.01,
    change: function(event, ui) {
        if (event.originalEvent) {
            if (source && playing) {
                source.stop();
                clearInterval(timer);
                var new_val = ui.value;
                process(reqData, mp3_time * new_val / 100);
            }

        }
    }
});

var mp3_time;
var timer;
var source;
var reqData;
var playing = false;
var first = true;

$('.generate').click(function(event) {
    if (first) {
        loadSound(0);
        playing = true;
        first = false;
    } else if (playing) {
        source.stop();
        ticker.slider('option', 'value', 0);
        clearInterval(timer);
        loadSound(0);
    } else {
        clearInterval(timer);
        ticker.slider('option', 'value', 0);
        loadSound(0);
    }
});

$('#button_play').click(function(event) {
    if (playing) {
        source.stop();
        clearInterval(timer);
    } else {
        var value = ticker.slider("option", "value");
        process(reqData, value);
    }

    playing = !playing;
});

function tickSlider() {
    var value = ticker.slider("option", "value");
    if (value + 100 / mp3_time > 100) {
        clearInterval(timer);
        return;
    }
    ticker.slider('option', 'value', value + 100 / mp3_time)
}


function loadSound(startTime) {
    var request = new XMLHttpRequest();
    request.open("GET", "/music", true);
    request.responseType = "arraybuffer";

    request.onload = function() {
        reqData = request.response;
        process(reqData, startTime);
    };

    request.send();
}

function process(Data, startTime) {
    source = context.createBufferSource(); // Create Sound Source
    context.decodeAudioData(Data, function(buffer) {
        source.buffer = buffer;
        source.connect(context.destination);
        source.start(context.currentTime, startTime);
        mp3_time = buffer.duration;
        timer = setInterval(function() { tickSlider() }, 1000);
    });
}
