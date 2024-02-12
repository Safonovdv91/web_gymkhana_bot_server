

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
        sport_class: "C3"
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



/*
fetch('http://127.0.0.1:8000/api/v1/users', {
  method: 'GET',
  credentials: 'include',
})
  .then(response => {

    return response.json()
  })
  .then(json => {

    json.data.forEach(user => {
      let userId = user.id
      let formUser = document.getElementsByClassName('user');
      for (let elem of formUser) {                                       // перебор html форм class="user"
        let formId = elem.getAttribute('data-userid')
        if (userId == formId) {

          let ggpClasses = elem.getElementsByClassName('ggp-classes-sub');
          for (let elem of ggpClasses) {
            console.log(elem.textContent)
            if (elem.textContent == user.ggp_sub_classes) {
              console.log(elem)
            }

            for 

          }


          console.log(user.ggp_sub_classes)
        }
      }
    });


  })
  .catch(error => console.log(error))

  */