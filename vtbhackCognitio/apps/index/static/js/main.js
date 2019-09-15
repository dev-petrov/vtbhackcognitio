const serv_ip = '192.168.43.201:8000';
let doc_id;
if (document.querySelector('#document_id')) {
    doc_id = document.querySelector('#document_id').textContent;
}

function yes() {
    var req = new XMLHttpRequest();

    req.open('POST', '/api/add_result/' + doc_id);
    req.onload = () => {
        console.log(req.response)
        var res = JSON.parse(req.response);
        console.log(res["prev"])
        document.querySelector('#user_point').innerHTML = `<p class='text-success'>Вы проголосвали за</p>`
        if (res["prev"] == 0){
            console.log('prev null')
            var yes = document.querySelector('#yes')
            var numYes = parseInt(yes.textContent)
            var no = document.querySelector('#no')
            var numNo = parseInt(no.textContent)
            yes.textContent = numYes + 1
            no.textContent = numNo - 1
        }
    }
    var data = new FormData();
    data.append('result', 1);
    data.append('user', getCookie('user'));
    req.send(data);
}

function no() {
    var req = new XMLHttpRequest();

    req.open('POST', '/api/add_result/' + doc_id);
    req.onload = () => {
        console.log(req.response)
        var response = JSON.parse(req.response);
        document.querySelector('#user_point').innerHTML = `<p class='text-danger'>Вы проголосвали против</p>`
        if (response['prev'] === 1){
            var yes = document.querySelector('#yes')
            var numYes = parseInt(yes.textContent)
            var no = document.querySelector('#no')
            var numNo = parseInt(no.textContent)
            yes.textContent = numYes - 1
            no.textContent = numNo + 1
        }
    }
    var data = new FormData();
    data.append('result', 0);
    data.append('user', getCookie('user'));
    req.send(data);
}
///////////////////////////////////////////////////////////////////////////

/*var time=5*60*60,r=document.getElementById('r'),tmp=time;

setInterval(function(){
var c=tmp--,h=(c/3600)»0,m=(c/60)»0,s=(c-m*60)+'';
r.textContent='Registration closes in '+h+':'+m+':'+(s.length>1?'':'0')+s
tmp!=0||(tmp=time);
},1000);*/
/////////////////////////////////

///////////////////////////////////////////////////////////////////////////

function check_correctivity(event) {
    event.preventDefault();
    //var err = document.querySelector('#error');
    //err.textContent = 'EEEERRROOORRRR';
    //err.setAttribute("style", "padding:10px;border: 1px solid red;display:blockmarginLeft:auto;marginRight:auto;width:50%;color:red;textAlign:center;backgroundcolor:lightred;");
    var data = new FormData(document.querySelector('#f'));
    var socket = new WebSocket("ws://" + serv_ip + "/api/get_comments/");
    socket.onopen = function () {
        socket.send("asde");
    };
    var ans;
    socket.onmessage = (e) => {
        ans = JSON.parse(e.data);
    }
    if (ans['type'] === 'success') {
        window.location.replace('/docs/');
    } else {
        var err = document.querySelector('#error');
        err.textContent = 'Вы ввели неверный логин или пароль!';
        err.className("error");
        document.querySelector('#pss').value = '';
    }
};
if (document.querySelector('#but')) {
    var but = document.querySelector('#but');
    but.onclick = check_correctivity;
} else {
    console.log('u\'r smart');
}

//////////////////////////////////////////////////////////////
if (document.querySelector('#textarea')) {
    textarea.scrollTo({
        top: 1000,
        behavior: "smooth"
    });
    get_messeges();
    get_results();
}

function post_message() {
    var req = new XMLHttpRequest();
    req.open('POST', '/api/add_comment/' + doc_id);////////////id stat'i
    req.onload = () => {
        var ans = JSON.parse(req.response);
        var least = document.querySelector('#chat');
        console.log(least);
        var tag = document.createElement("div");
        tag.className = 'row';
        var intag1 = document.createElement("div");
        intag1.className = 'col-3 username';
        var cont = document.createTextNode(ans['first_name'] + ' ' + ans['last_name']);
        intag1.appendChild(cont);
        var intag2 = document.createElement("div");
        intag2.className = 'col-5 comment';
        cont = document.createTextNode(ans['text']);
        intag2.appendChild(cont);
        var intag3 = document.createElement("div");
        intag3.className = 'col-4 date';
        cont = document.createTextNode(ans['date']);
        intag3.appendChild(cont);
        tag.appendChild(intag1);
        tag.appendChild(intag2);
        tag.appendChild(intag3);
        //tag.appendChild(cont);
        //var element = document.getElementById("div1");
        least.appendChild(tag);
        textarea.scrollTo({
            top: 1000,
            behavior: "smooth"
        });
    }
    var date = new Date();
    var data = new FormData();
    var comment = document.querySelector('#message');
    data.append('text', comment.value)
    console.log(date);
    req.send(data/* + '|' + date.getFullYear() + '-'
+ date.getMonth() + '-' + date.getDate() + ' ' + date.getHours() + ':' +
date.getMinutes() + ':' + date.getSeconds()*/);
    comment.value = '';
}

function get_messeges() {
    //console.log('some gay shit');
    //var data = new FormData(document.querySelector('#f'));
    date = new Date();
    var socket = new WebSocket("ws://" + serv_ip + "/api/get_comments/");
    socket.onopen = function () {
        json = {
            'date':date.getFullYear() + '-'
            + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' +
            date.getMinutes() + ':' + date.getSeconds(),
            'doc_id': doc_id,
            'user' : getCookie('user')
        }
        json = JSON.stringify(json)
        console.log(json)
        socket.send(json);
    };
    var ans;
    socket.onmessage = (e) => {
        ans = JSON.parse(e.data);
        console.log(e.data)
        date = new Date()
        json = {
            'date':date.getFullYear() + '-'
            + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' +
            date.getMinutes() + ':' + date.getSeconds(),
            'doc_id': doc_id,
            'user' : getCookie('user')
        }
        json = JSON.stringify(json)
        console.log(json)
        socket.send(json);

        if (ans['type'] === 'nothing new') {
            return
        } else {
            var comments = ans['comments'];
            for (var i = 0; i < comments.length; i++) {
                var least = document.querySelector('#chat');
                console.log(least);
                var tag = document.createElement("div");
                tag.className = 'row';
                var intag1 = document.createElement("div");
                intag1.className = 'col-3 username';
                var cont = document.createTextNode(comments[i]['user']['first_name'] + ' ' + comments[i]['user']['last_name']);
                intag1.appendChild(cont);
                var intag2 = document.createElement("div");
                intag2.className = 'col-5 comment';
                cont = document.createTextNode(comments[i]['text']);
                intag2.appendChild(cont);
                var intag3 = document.createElement("div");
                intag3.className = 'col-4 date';
                cont = document.createTextNode(comments[i]['date']);
                intag3.appendChild(cont);
                tag.appendChild(intag1);
                tag.appendChild(intag2);
                tag.appendChild(intag3);
                //tag.appendChild(cont);
                //var element = document.getElementById("div1");
                least.appendChild(tag);
                
            }
        }
    }
}
function get_results() {
    //console.log('some gay shit');
    //var data = new FormData(document.querySelector('#f'));
    date = new Date();
    var socket = new WebSocket("ws://" + serv_ip + "/api/get_results/");
    socket.onopen = function () {
        json = {
            'date':date.getFullYear() + '-'
            + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' +
            date.getMinutes() + ':' + date.getSeconds(),
            'doc_id': doc_id,
            'user' : getCookie('user')
        }
        json = JSON.stringify(json)
        console.log(json)
        socket.send(json);
    };
    var ans;
    socket.onmessage = (e) => {
        ans = JSON.parse(e.data);
        console.log(e.data)
        date = new Date()
        json = {
            'date':date.getFullYear() + '-'
            + (date.getMonth() + 1) + '-' + date.getDate() + ' ' + date.getHours() + ':' +
            date.getMinutes() + ':' + date.getSeconds(),
            'doc_id': doc_id,
            'user' : getCookie('user')
        }
        json = JSON.stringify(json)
        console.log(json)
        socket.send(json);

        if (ans['type'] === 'nothing new') {
            return
        } else {
            var results = ans['results'];
            for (var i = 0; i < results.length; i++) {
                console.log(results)
                var new_res = document.querySelector('#user' + results[i]['user']['id']);
                if (results[i]['result'] == 0){
                    new_res.innerHTML = `<p class='text-danger'>Против</p>`;
                    var yes = document.querySelector('#yes');
                    var numYes = parseInt(yes.textContent);
                    var no = document.querySelector('#no');
                    var numNo = parseInt(no.textContent);
                    yes.textContent = numYes - 1;
                    no.textContent = numNo + 1;
                } else {
                    new_res.innerHTML = `<p class='text-success'>За</p>`;
                    var yes = document.querySelector('#yes');
                    var numYes = parseInt(yes.textContent);
                    var no = document.querySelector('#no');
                    var numNo = parseInt(no.textContent);
                    yes.textContent = numYes + 1;
                    no.textContent = numNo - 1;
                }

                
            }
        }
    }
}

///////////////////////////////////////////////////
if (document.querySelector('#dropping_list')) {
    var inp = document.querySelector('#istream')
    inp.oninput = function dynamic_search() {
        var req = new XMLHttpRequest();
        req.open('POST', '/api/search/');
        req.onload = () => {
            var ans = JSON.parse(req.response)
            if (ans['type'] === 'found') {
                for (var i = 0; i < ans['data'].length(); i++) {
                    var tag = document.createElement('li');
                    var cont = document.createTextNode(ans['data'][i][0]);
                    tag.appendChild(cont);
                    var intag = document.createElement('a');
                    cont = document.createTextNode(ans['data'][i][1]);
                    intag.appendChild(cont);
                    intag.setAttribute('href', '/docs/' + ans['data'][i][1]);
                    tag.appendChild(intag);
                    document.querySelector('#dropping_list').appendChild(tag);
                }
            } else { return }
        }
        req.send(inp.value);
        //console.log(inp.value);
    }
}
function decode_utf8(s) {
    return decodeURIComponent(escape(s));
  }

  function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }