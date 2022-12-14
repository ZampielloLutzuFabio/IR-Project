const Rating = {
    Relevant: 'Relevant',
    Irrelevant: 'Irrelevant'
};

localStorage.setItem('relevant', JSON.stringify([]));
localStorage.setItem('irrelevant', JSON.stringify([]));

function toggleFilters() {
    var filterFields = document.getElementsByClassName('filter');
    for (var i = 0; i < filterFields.length; i++) {
        if (filterFields[i].style.display === "none") {
            filterFields[i].style.display = "inline";
        } else {
            filterFields[i].style.display = "none";
        }
    }
}

function quote(obj) {
    var return_val = '((';
    var firstElem = true;

    for (const [key, value] of Object.entries(obj)) {
        if (!Array.isArray(value)) {
            value = [value]
        }

        value.forEach(val => {
            if (firstElem) {
                return_val += '(' + key + ':*' + val + '*)';
                firstElem = false
            } else {
                return_val += 'OR(' + key + ':*' + val + '*)'
            }
        })
    }

    return return_val;

}

function quote_filter(obj) {
    if (Object.keys(obj).length == 0) {
        return "))";
    }

    var return_val = ")";

    for (const [key, value] of Object.entries(obj)) {
        if (!value || (value.length == 1 && !value[0])) {
            continue;
        } else {
            if (!Array.isArray(value)) {
                value = [value]
            }
            value.forEach(val => {
                return_val += 'AND(' + key + ':*' + val + '*)';
            })
        }
    }

    return_val += ")"

    return return_val;

}

function openLink(url) {
    window.open(url, '_blank');
}

function populate_table(array, query) {
    console.log('before ', array);

    var irr_arr = JSON.parse(localStorage.getItem('irrelevant'));
    var rel_arr = JSON.parse(localStorage.getItem('relevant'));

    var tmp_irr = [];
    var tmp_rel = [];
    var i = 0;
    while (i < array.length){
        if (irr_arr.includes(array[i]['id'])) {
            tmp_irr.push(array[i]);
            array.splice(i, 1)
            continue;
        }

        if (rel_arr.includes(array[i]['id'])) {
            tmp_rel.push(array[i]);
            array.splice(i, 1);
            continue;
        }

        i = i + 1;
    }

    for (var i = 0; i < tmp_irr.length; i++){ 
        array.push(tmp_irr[i]);
    }

    for (var i = 0; i < tmp_rel.length; i++){ 
        array.unshift(tmp_rel[i]);
    }



    console.log('after ', array);

    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera

    var table = document.querySelector('table');
    var tutorialBox = document.querySelector('#tutorial');
    var tableBody = document.querySelector('tbody');

    var t = "";

    for (var i = 0; i < array.length; i++) {
        if (array[i]['genre'] === undefined) {
            array[i]['genre'] = ['No Genre'];
        }

        array[i]['title'] = array[i]['title'].join(',');
        array[i]['author'] = array[i]['author'].join(',');
        array[i]['genre'] = array[i]['genre'].slice(0, 5).join(',');
        array[i]['platform'] = array[i]['platform'].join(',');
        array[i]['price'] = array[i]['price'].join(',');
        array[i]['sale'] = array[i]['sale'].join(',');
        array[i]['description'] = array[i]['description'].join(',');

        query.forEach(q => { array[i]['title'] = array[i]['title'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['author'] = array[i]['author'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['genre'] = array[i]['genre'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['platform'] = array[i]['platform'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['price'] = array[i]['price'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['sale'] = array[i]['sale'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });
        query.forEach(q => { array[i]['description'] = array[i]['description'].replaceAll(new RegExp(q, 'gi'), `<b>${q}</b>`) });

        var tr = `<tr id=${array[i]['id']}>`;
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['title'] + "</td>";
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['author'] + "</td>";
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['genre'] + "</td>";
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['platform'] + "</td>";
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['price'] + "</td>";
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['sale'] + "</td>";
        tr += '<td onclick=openLink("' + array[i]['href'] + '")>' + array[i]['description'] + "</td>";
        tr += "<td>" + `<button onclick=make_relevant("${array[i]['id']}")>&#128077;</button>` + "</td>";
        tr += "<td>" + `<button onclick=make_irrelevant("${array[i]['id']}")>&#128078;</button>` + "</td>";
        tr += "</tr>";
        t += tr;
    }

    if (t.length == 0) {
        t += "<tr>";
        t += "<td colspan='7' id='no_results'>No Results Were Found</td>";
        t += "</tr>";
    }

    tableBody.innerHTML = t;

    for (var i = 0; i < rel_arr.length; i++) {
        var tmp = document.getElementById(rel_arr[i]);
        if (tmp) {
            tmp.classList.add('relevant');
        }
    }
    for (var i = 0; i < irr_arr.length; i++) {
        var tmp = document.getElementById(irr_arr[i]);
        if (tmp) {
            tmp.classList.add('irrelevant');
        }
    }

    if (table.style.display === "none") {
        table.style.display = "block";
        tutorialBox.style.display = "none";
    }
}

function make_relevant(id) {
    console.log(`make relevant ${id}`);

    var irr_arr = JSON.parse(localStorage.getItem('irrelevant'));
    if (irr_arr.indexOf(id) > -1) {
        irr_arr.splice(irr_arr.indexOf(id), 1);
    }
    localStorage.setItem('irrelevant', JSON.stringify(irr_arr));

    var rel_arr = JSON.parse(localStorage.getItem('relevant'));
    if (rel_arr.indexOf(id) > -1) {
        rel_arr.splice(rel_arr.indexOf(id), 1);
        document.getElementById(id).classList.remove('relevant');
    } else {
        rel_arr.push(id);

        var tableBody = document.querySelector('tbody');
        var tableRowHTML = document.getElementById(id).innerHTML;
        document.getElementById(id).remove();
        tableBody.innerHTML = `<tr id=${id} class='relevant'>` + tableRowHTML + `</tr>` + tableBody.innerHTML;
    }

    localStorage.setItem('relevant', JSON.stringify(rel_arr));
}

function make_irrelevant(id) {
    console.log('make irrelevant ' + id);

    var tableBody = document.querySelector('tbody');
    var tableRowHTML = document.getElementById(id).innerHTML;
    document.getElementById(id).remove();
    tableBody.innerHTML = tableBody.innerHTML + `<tr id=${id} class='irrelevant'>` + tableRowHTML + `</tr>`;

    var rel_arr = JSON.parse(localStorage.getItem('relevant'));
    if (rel_arr.indexOf(id) > -1) {
        rel_arr.splice(rel_arr.indexOf(id), 1);
    }
    localStorage.setItem('relevant', JSON.stringify(rel_arr));

    var irr_arr = JSON.parse(localStorage.getItem('irrelevant'));
    if (irr_arr.indexOf(id) > -1) {
        irr_arr.splice(irr_arr.indexOf(id), 1);
        document.getElementById(id).classList.remove('irrelevant');
    } else {
        irr_arr.push(id);

        var tableBody = document.querySelector('tbody');
        var tableRowHTML = document.getElementById(id).innerHTML;
        document.getElementById(id).remove();
        tableBody.innerHTML = tableBody.innerHTML + `<tr id=${id} class='irrelevant'>` + tableRowHTML + `</tr>`;
    }

    localStorage.setItem('irrelevant', JSON.stringify(irr_arr));
}


function search() {
    var url = 'http://localhost:8983/solr/indiegames/query?rows=1000&q=';

    var query = document.getElementById('searchGame').value.split(',');
    for (var i = 0; i < query.length; i++) {
        query[i] = query[i].trim();
    }

    var obj = {
        title: query,
        platform: query,
        author: query,
        genre: query
    }

    var filter = {
        genre: document.getElementById('genreFilter').value.split(","),
        price: document.getElementById('priceFilter').value.split(","),
        sale: document.getElementById('saleFilter').value.split(","),
        author: document.getElementById('authorFilter').value.split(","),
        platform: document.getElementById('platformFilter').value.split(","),
    }

    url += encodeURI(quote(obj) + quote_filter(filter));

    console.log(url);

    fetch(url, {
        method: "GET",
        headers: {
            Accept: 'application/json'
        }
    }).then(function (response) {
        return response.json();
    }).then(data => {
        populate_table(data.response.docs, query);
        localStorage.setItem('array', JSON.stringify(data.response.docs));
    });

}

var inputs = document.querySelectorAll('input');

for (var input of inputs) {
    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            document.getElementById("searchButton").click();
        }
    });
}