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

// сворачивание кнопок классов


let coll = document.getElementsByClassName('collaps')

for (let i = 0; i < coll.length; i++) {
  coll[i].addEventListener('click', function (event) {
    event.preventDefault();
    console.log('click')
    this.classList.toggle('active');
    let content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + 'px'
    }
  })
}


//медот PATCH запроса

(function asd() {

  function onSubmit(event) {

    event.preventDefault();
    console.log('Отправка!')

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

function handleClickFunction(event) {
  event.target.classList.toggle('active');
}

for (let element of elements) {
  element.addEventListener('click', handleClickFunction)
}

fetch(`${AppConsts.BaseUrl}/api/v1/users`, {
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


            user.ggp_sub_classes.forEach(classLetter => {
              console.log(classLetter.sport_class)
              if (elem.textContent == classLetter.sport_class) {
                elem.classList.add('active')
              }
            })
          }
        }
      }
    });


  })
  .catch(error => console.log(error))


// delete-post-запрос

const exit = document.getElementById('patch-button-exit')
exit.addEventListener('click', onSubmitExit);

// объявляем константу с URL-адресом, на котрый будет отправляться запрос
const requestURL = `${AppConsts.BaseUrl}/auth/jwt/logout`;

// создаём функцию, в которой объявляем переменные, условие и делаем запрос
async function onSubmitExit(event) {

  //отмена действия браузера, чтобы он ничего не делал, пока юзер на нажмёт на кнопку
  event.preventDefault();

  // создаётся ф-я запроса методом FETCH, с Асинхронным запросом
  let response = await fetch(requestURL, {
    method: 'POST',
    headers: {
      'Accept': 'application/json'
      },
      body: JSON.stringify({})
  });



  // проверка статуса для вывода сообщения о результате выполнения запроса(ошибка или успех)
  if (response.status == 200) {
    alert('Success')
    window.location = "login";

  } else if (response.status == 204) {
    alert('No content')
    window.location = "login";

  } else if (response.status == 401) {

    alert('Inactive user');

  } else console.log('Что-то пошло нетак, обратитесь в поддержку');

};
