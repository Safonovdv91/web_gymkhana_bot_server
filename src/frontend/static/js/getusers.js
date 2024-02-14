function updateStatementGGPSubscribing(){
  console.log('Обновляем данные о GGP')
  fetch(`${AppConsts.BaseUrl}/api/v1/users`, {
  method: 'GET',
  credentials: 'include',
})
  .then(response => {
    return response.json()
  })
  .then(json => {
    json.data.forEach(user => updateSubGGPClasses(user));
  })
  .catch(error => console.log(error))
}

// Метод обновления состояния буковки подписки класса
function updateSubGGPClasses(user) {
      let userId = user.id
      let formUser = document.getElementsByClassName('user');
      for (let elem of formUser) {                                       // перебор html форм class="user"
        let formId = elem.getAttribute('data-userid')
        if (userId == formId) {
          let ggpClasses = elem.getElementsByClassName('ggp-classes-sub');
          for (let elem of ggpClasses) {
            user.ggp_sub_classes.forEach(classLetter => {
              if (elem.textContent == classLetter.sport_class) {
                elem.classList.add('active')
              }
            })
          }
        }
      }
    }

// функция подписки на классы в соответствии с логикой
function patchSubGGPClasses(event,operation,literal) {
    let button = event.target;
    const userid = button.dataset.userid;
    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/subscribe`, {
      method: 'PATCH',
      body: JSON.stringify({
        op: operation,
        sport_class: literal,
      }),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      }
    })
      .then(response => response.json())
      .then(json => console.log(json.details))
}

// Переключатель свечения кнопки и выбора метода
function handleClickFunction(event) {
  event.target.classList.toggle('active');
  if (event.target.getAttribute('class').includes('active')) {
    patchSubGGPClasses(event,'add', event.target.innerText)
  } else {
    patchSubGGPClasses(event,'remove', event.target.innerText)
  }
}

// метод DELETE запроса - это переделать
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

updateStatementGGPSubscribing()
const elements = document.getElementsByClassName('ggp-classes-sub')

for (let element of elements) {
element.addEventListener('click', handleClickFunction)
}

