(function asd() {
  //медот PATCH запроса
  let onSubmit = function (event) {

    event.preventDefault();

    let button = event.target;

    const userid = button.dataset.userid;

    fetch(`/api/v1/users/id=${userid}/subscribe`, {
      method: 'PATCH',
      body: JSON.stringify({
        sport_class: "B",
      }),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      }
    })
      .then(response => response.json())
      .then(json => console.log(json.detail))
  }

  let elements = document.getElementsByClassName('patch-button-submit');

  for (let element of elements) {
    element.addEventListener('click', onSubmit);
  }


  // метод GET запроса
  /*fetch('http://127.0.0.1:8000/api/v1/users',  {
    method: 'GET',
    credentials: 'include',
  })
        .then(response => {
          console.log(response)
          return response.json()
        })
        .then(json => {
          console.log(json.data[0].email);
          
          let emailElement = document.querySelector('#user-email');
          emailElement.textContent = json.data[0].email;
  
        })
        .catch(error => console.log(error))*/
})();

