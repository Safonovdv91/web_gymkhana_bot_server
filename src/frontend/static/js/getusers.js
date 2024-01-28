
document.getElementById('patch-button').addEventListener('submit', onSubmit);

const requestURL =`${AppConsts.BaseUrl}/auth/register`;

async function onSubmit(event) {


    event.preventDefault();

    let response = await fetch('https://site.com/service.json', {
    method: 'PATCH',
    headers: {
        'Content-Type': 'application/json',
        'API-Key': 'secret'
    }
    });


    let result = await response.json();
    console.log(JSON.stringify(result));
}