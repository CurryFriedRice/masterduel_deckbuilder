function generate_small_card(data)
{
    return `
        <img src="/static/img/card_image_small/${data['pin']}.jpg">
    `
}


async function search(e){
    e.preventDefault();
    var searchForm = document.getElementById('searchForm')
    var form = new FormData(searchForm);

    var search = await fetch('/card/search',{method:'POST',body:form}) //, {method: 'POST', body: form})
        .then(res => res.json())
        .then(data => {
            console.log(form)
            console.log(data)
            html = ``
            for (var dat of data['data'])
            {
                html += generate_small_card(dat)
            }


            document.querySelector("#searchOutput").innerHTML = html
        })
    }

async function createAccount(e)
{
        e.preventDefault()
        var form = new FormData(document.querySelector("#accountCreationForm"))
        var req= await fetch("/account/create",{method:"POST", body: form})
                        .then(res  => {
                            if (res.redirected) window.location.reload() 
                            return res.json()
                        })
                        .then(data => {
                            if (data['error'])
                            {
                                err = data['error']
                                //console.log(data['error']['account_email_err'])
                                document.querySelector(`#account_username_err`).innerText = err['account_username_err'] ? err['account_username_err']  : ''
                                document.querySelector(`#account_email_err`).innerText = err['account_email_err'] ? err['account_email_err']  : ''
                                document.querySelector(`#account_password_err`).innerText = err['account_password_err'] ? err['account_password_err']  : ''
                                document.querySelector(`#account_eula_err`).innerText = err['account_eula_err'] ? err['account_eula_err']  : ''
                            }
                            else fetch("/dashboard")
                        })
}
    
async function login(e)
{
        e.preventDefault()
        var form = new FormData(document.querySelector("#loginForm"))
        var req= await fetch("/account/login",{method:"POST", body: form})
        .then(res  => {
            if (res.redirected) window.location.reload() 
            return res.json()
        })
        .then(data => {
            //console.log("HELP I NEED TO LOG IN")
            if (data.hasOwnProperty("error"))
            {
                err = data['error']
                document.querySelector(`#login_err`).innerText = err['login_err'] ? err['login_err']  : ''
            }            
        })
}
    