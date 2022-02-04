
var holdingCard = false
var searchResults
var targetCardID
var detailed = false
var deck = { "main": {}, "extra": {} }


async function search(e) {
    e.preventDefault();
    var searchForm = document.getElementById('searchForm')
    var form = new FormData(searchForm);
    var search = await fetch('/card/search', { method: 'POST', body: form }) //, {method: 'POST', body: form})
        .then(res => res.json())
        .then(data => {
            // console.log(searchResults)
            // console.log(form)
            // console.log(data)
            html = ``
            searchResults = data['data'];
            if ('error' in data) {
                document.querySelector("#searchOutput").innerHTML = `<h1>${data['error']}</h1>`
            }
            else {
                for (var dat of data['data']) {
                    html += generate_small_card(dat)
                }
                document.querySelector("#searchOutput").innerHTML = html
                console.log(document.querySelectorAll(".card"))
            }

            // for (var item of document.querySelectorAll(".card")){
            //     item.addEventListener("mousedown", selectCard);
            //     item.addEventListener('mouseover', mouseEnterCard);
            //     item.addEventListener('mouseout', mouseExitCard);
            //     item.addEventListener('keydown', keyDownDoc)
            //     //console.log(item)
            // }
        })
}

async function submitDeck(e) {
    e.preventDefault()
    var deckDetails = document.getElementById("details")
    var data = new FormData(deckDetails);
    data.append("deck", JSON.stringify(deck))
    //TODO: Do some prevalidation before we ask the server to check it....
    console.log(data)
    // form.append ("deck", deck)  
    var string = window.location.href
    string = string.substring(0,string.indexOf("/edit"))
    console.log(string)
    var submit = await fetch(`${string}/update`, { method: 'POST', body: data })
        .then(res => {
            if (res.redirected) window.location = res.url;
            return res.json()
        })
        .then(data => {
            console.log(data)
            errorText = ``
            for (items in data['error'])
                errorText += `<p>ERROR: ${data['error'][items]}</p>`
            document.getElementById("errorOutput").innerHTML = errorText
        })
}

function generate_small_card(data) {
    return `
    <div>
        <img src="/static/img/card_image_small/${data['pin']}.jpg" 
            class='card'
            card_pin='${data['pin']}'
            onmousedown = 'grabCard(event)'
            onmouseover = 'mouseEnterCard(event)'
            onmouseout  = 'mouseExitCard(event)'
        >
    </div>
    `
}

function generate_details_card(data) {
    console.log(data)
    return `<img src='/static/img/card_image/${data['pin']}.jpg'>
    <h1>${data['name']}</h1>
    <h1>${data['level']}</h1>
    <h1>${data['attribute']}<h1>
    <h1>${data['description']}</h1>
    <h1>${data['attack']}</h1>
    <h1>${data['defense']}</h1>
    <h1>${data['race']}</h1>
    <h1>${data['type']}</h1>`
}

function renderDeck(deckValue) {
    console.log(`rendering Deck with cards ${deckValue['main']}`)

    var renderItem = ``
    for (const key in deckValue['main']) {
        console.log(`${key} | ${deckValue['main'][key]}`)
        for (var count = 0; count < deckValue['main'][key]; count++) {
            renderItem += generate_small_card({ "pin": key })
        }
    }
    document.querySelector(`#mainDeck`).querySelector(".display").innerHTML = renderItem

    renderItem = ''
    for (const key in deckValue['extra']) {
        console.log(`${key} | ${deckValue['extra'][key]}`)
        for (var count = 0; count < deckValue['extra'][key]; count++) {
            renderItem += generate_small_card({ "pin": key })
        }
    }
    document.querySelector(`#extraDeck`).querySelector(".display").innerHTML = renderItem


}

function grabCard(e) {
    e.preventDefault()
    holdingCard = true
}


function addCard() {
    if (targetCardID != null) {
        // console.log("Called to adda  card")
        // console.log(`The cardID is ${targetCardID}`)
        fetch(`/card/${targetCardID}.json`)
            .then(res => res.json())
            .then(data=> {
                //if ([20, 21, 22, 23, 25, 24, 26, 27].includes(data.type)) {
                var target = 'main'
                //if (['Fusion Mosnter', 'Link Monster', 'Pendulum Effect Fusion Monster', 'Synchro Monster', 'Synchro Pendulum Effect Monster', 'Synchro Tuner Monster', 'XYZ Monster', 'XYZ Pendulum Effect Monster'].includes(data.type)) target = 'extra';
                if ([20, 21, 22, 23, 25, 24, 26, 27].includes(data.type_id)) target = 'extra'
                
                if (data.pin in deck[target] && deck[target][data.pin] < 3)
                    deck[target][data.pin] += 1
                    else if (deck[target][data.pin] >= 3) {
                        deck[target][data.pin] = 3
                        document.querySelector("#errorOutput").innerHTML = `<p>Max copies of card is 3</p>`
                        setTimeout(function(e){document.querySelector("#errorOutput").innerHTML = ``},10000)
                    }
                    else //If it does not then we'll create it and set it to one
                    {
                        console.log(data.pin)
                        deck[target][data.pin] = 1
                    }
                renderDeck(deck)
            })
        }
}

function subtractCard() {
    if (targetCardID != null) {

        var target = (targetCardID in deck['main']) ? 'main' : 'extra'
            deck[target][targetCardID] <= 1 ? delete deck[target][targetCardID] : deck[target][targetCardID] = deck[target][targetCardID] - 1

        renderDeck(deck)
    }
}


function mouseEnterCard(event) {
    event.preventDefault()
    if (!holdingCard) {
        targetCardID = event.target.getAttribute('card_pin')
        console.log(`Mouse Over: ${targetCardID}`);
    }
    if (detailed) {
        fetch(`/card/${targetCardID}.json`)
            .then(res => res.json())
            .then(data => {
                var innerHTML = generate_details_card(data)
    
                document.querySelector("#cardDetails").innerHTML = innerHTML
            })
    }
}
function mouseExitCard(event) {
    event.preventDefault()
    if (!holdingCard) {
        targetCardID = null
        console.log(`Mouse out: ${targetCardID}`);
    }
}

async function keyDownDoc(e) {

    var input = e.key;

    console.log(`keypress: ${input} |TCID: ${targetCardID}`)
    if (targetCardID != null) {
        if (input === 'a') {
            console.log("add card to Deck")
            addCard()
        } else if (input === "s") {
            console.log("Remove Card from deck")
            subtractCard()
        } else if (input === 'd') {
            console.log("enable detailed View")
            detailed = !detailed
            if (!detailed)
                document.querySelector("#cardDetails").innerHTML = ``
        }
    }
}


document.addEventListener("mouseup", function (e) {
    holdingCard = false;
    targetCardID = null
    console.log(`holdingCard: ${holdingCard} | TCID ${targetCardID}`)
})


document.querySelector("#deckSide").addEventListener("mouseup", addCard)

document.addEventListener("mouseover", function (e) {
    origin = "deck"
})

document.querySelector("#searchSide").addEventListener("mouseup", subtractCard)
document.addEventListener("mouseover", function (e) {
    origin = "search"
})

document.addEventListener('keydown', keyDownDoc)
document.querySelector("#mainDeck").addEventListener('keydown', keyDownDoc)
document.querySelector("#extraDeck").addEventListener('keydown', keyDownDoc)
// fetch("/card/91152256.json").then(res=>res.json()).then(data=> console.log(data))

fetch(window.location.href.replace("/edit","/json")).then(res=>res.json()).then(data=> {
    for(const item in data['deck'])
        for(let c = 0; c < data['deck'][item]; c++)
            prebuildDeck(item)

    document.getElementById("details").querySelector('input[name="name"]').value = data['details']['name'];
    document.getElementById("details").querySelector('textarea[name="playstyle"]').value = data['details']['description'];
})




function prebuildDeck(card_pin) {
   
    fetch(`/card/${card_pin}.json`)
        .then(res => res.json())
        .then(data=> {
            //if ([20, 21, 22, 23, 25, 24, 26, 27].includes(data.type)) {
            var target = 'main'
            //if (['Fusion Mosnter', 'Link Monster', 'Pendulum Effect Fusion Monster', 'Synchro Monster', 'Synchro Pendulum Effect Monster', 'Synchro Tuner Monster', 'XYZ Monster', 'XYZ Pendulum Effect Monster'].includes(data.type)) target = 'extra';
            if ([20, 21, 22, 23, 25, 24, 26, 27].includes(data.type_id)) target = 'extra'
            
            if (data.pin in deck[target] && deck[target][data.pin] < 3)
                {
                    deck[target][data.pin] += 1
                }
                else //If it does not then we'll create it and set it to one
                {
                    console.log(data.pin)
                    deck[target][data.pin] = 1
                }
            renderDeck(deck)
        })
}
