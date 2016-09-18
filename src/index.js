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

$('button').click(function(event) {
	var value = ticker.slider("option", "value");
    loadSound(value);
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
    request.open("GET", "http://localhost:9000/music", true);
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
