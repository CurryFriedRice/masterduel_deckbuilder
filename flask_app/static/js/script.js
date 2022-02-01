async function search(e){
    e.preventDefault();
    var searchForm = document.getElementById('searchForm')
    var form = new FormData(searchForm);

    var search = await fetch('/card/search',{method:'POST',body:form}) //, {method: 'POST', body: form})

    // fetch('/card/search',{method:'POST',body:form})
    //     .then(res => res.json() )
    //     .then( data => {
    //         console.log(form)
    //         console.log(data)
            // let retHTML = ``
            // for (const values of data)
            // {
            //     retHTML += `
            //         <div class='m-2'>
            //             <h1>${values['name']}</h1>
            //         </div>
            //     `
            // }
            // document.querySelector("#searchOutput").innerHTML = retHTML
        //})

}

async function update_archetypes(e)
{
    e.preventDefault();
    // let response =  await fetch("https://db.ygoprodeck.com/api/v7/archetypes.php");
    // var archetypes_list =  [{"archetype_name":"@Ignister"},{"archetype_name":"A.I."},{"archetype_name":"ABC"}]//response.json()
    // console.log(archetypes_list)
    // var form = new FormData(archetypes_list)
    var add_to_db = await fetch("/archetypes/setup")//, {method: 'POST', body: form})

}


// ("Normal"),
// ("Field"),
// ("Equip"),
// ("Continuous"),
// ("Quick-Play"),
// ("Ritual"),
// ("Counter");
// ("Normal"),
// ("Continuous"),


// ("Effect Monster"),
// ("Flip Effect Monster"),
// ("Flip Tuner Effect Monster"),
// ("Gemini Monster"),
// ("Normal Monster"),
// ("Normal Tuner Monster"),
// ("Pendulum Effect Monster"),
// ("Pendulum Flip Effect Monster"),
// ("Pendulum Normal Monster"),
// ("Pendulum Tuner Effect Monster"),
// ("Ritual Effect Monster"),
// ("Ritual Monster"),
// ("Skill Card"),
// ("Spell Card"),
// ("Spirit Monster"),
// ("Toon Monster"),
// ("Trap Card"),
// ("Tuner Monster"),
// ("Union Effect Monster"),

// ("Fusion Monster"),
// ("Link Monster"),
// ("Pendulum Effect Fusion Monster"),
// ("Synchro Monster"),
// ("Synchro Pendulum Effect Monster"),
// ("Synchro Tuner Monster"),
// ("XYZ Monster"),
// ("XYZ Pendulum Effect Monster");