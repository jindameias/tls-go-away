// ==UserScript==
// @name         tls
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @grant        none
// ==/UserScript==


!function () {
    // function w_reload(){
    //     window.location.reload()
    // }
    // setTimeout(w_reload, 10*600*1000)

    function create_xhr(method, url) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.timeout = 60*1000;
        return xhr
    }
    function xhr_something(xhr) {
        xhr.ontimeout = function () {
            websocket.send('this request timeout')
        };
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log(xhr.responseText);
                websocket.send(xhr.responseText)
            }
            else if (xhr.readyState === 4 && xhr.status > 200) {
                console.log(xhr.responseText);
                websocket.send('request error, the status is '+xhr.status)
            }
        };
    }

    function xgr(message) {
        let message_json = JSON.parse(message);
        let url = message_json.headers['Transpond-Url'] || location.href;
        if (message_json.method === 'GET') {
            let xhr = create_xhr(message_json.method, url);
            // add some operate, example:
            for (let key in message_json.headers){
                if (key.toUpperCase() === 'Businessid'.toUpperCase()){
                    xhr.setRequestHeader(key, message_json.headers[key])
                }
            }
            for (let key in message_json.cookies){
                document.cookie = key +"="+ message_json.cookies[key];
            }

            // add some operate, complete
            // add xhr status change behavior
            xhr_something(xhr);
            // add xhr status change behavior, complete
            xhr.send()
        }
        else if (message_json.method === 'POST') {
            let xhr = create_xhr(message_json.method, url);
            // add some operate, example
            for (let key in message_json.headers){
                if (key.toUpperCase() === 'Businessid'){
                    xhr.setRequestHeader(key, message_json.headers[key])
                }
            }
            // add xhr status change behavior
            xhr_something(xhr);
            // add xhr status change behavior, complete
            xhr.send()
        }
    }

    const websocket = new WebSocket("ws://127.0.0.1:9999/chrome_client");
    websocket.onopen = function () {
        console.log(location.href);
        websocket.send(location.href+'|'+(+new Date));
    };
    websocket.onmessage = function (e) {
        console.log(e);
        // xgr("https://tls.browserleaks.com/json", e.data)
        xgr(e.data)

    };
    websocket.onerror = function (e) {
          websocket.send(e);
    };
    websocket.onclose = function (e) {
          websocket.send('websocket_close');
    }
}();