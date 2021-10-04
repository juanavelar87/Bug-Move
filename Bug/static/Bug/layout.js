document.addEventListener('DOMContentLoaded', function() {
    load_animals();
    // document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
});
function load_animals()
{
    var content="<h1 style='padding:20px;'>Animals in your region</h1>"
    fetch("/Species")
    .then(response=>response.json())
    .then( animals =>{
        for (let i = 0; i < animals.length; i++) {
            content+=`
            <div class="animaldiv">
            
            <div style="width:100%">
            <h3 >${animals[i].Name}</h3>
            </div>
            <div style="width:100%">
            <ul>
    <li><h6>Common Name: ${animals[i].CommonName}</h6></li>
    <li><h6>Taxonomic Group: ${animals[i].TaxonomicGroup}</h6></li>
</ul>
            </div>
        </div>` 
        }
    document.querySelectorAll(".body")[0].innerHTML=content;

    })
}