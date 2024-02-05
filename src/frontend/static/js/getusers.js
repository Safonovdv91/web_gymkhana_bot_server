

//медот PATCH запроса

(function asd() {

  function onSubmit(event) {

    event.preventDefault();
    console.log('Отправка!')

    let button = event.target;

    const userid = button.dataset.userid;

    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/subscribe`, {
      method: 'PATCH',
      body: JSON.stringify({
        op: "add",
        sport_class: "A"
      }),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      }
    })
      .then(response => response.json())
      .then(json => console.log(json.details))
  }

  let elements = document.getElementsByClassName('patch-button-submit');

  for (let element of elements) {
    element.addEventListener('click', onSubmit);
  }
})();


// метод DELETE запроса

(function basd() {

  function onSubmit(event) {

    event.preventDefault();
    console.log('Отправка!')

    let button = event.target;

    const userid = button.dataset.userid;

    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/delete`, {
      method: 'DELETE'

    })
      .then(response => response.json())
      .then(json => console.log(json))
  }

  let elements = document.getElementsByClassName('delete-button-submit');

  for (let element of elements) {
    element.addEventListener('click', onSubmit);
  }
})();



// работа с кнопками классов

// отмена перезагрузки страницы после нажатия кнопки А
const form = document.querySelector('.A-class-button-submit')
form.addEventListener('click', (event) => {
    event.preventDefault()
})
