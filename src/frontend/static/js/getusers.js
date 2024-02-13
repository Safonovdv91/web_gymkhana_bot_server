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

function patchSubGGPClasses(event,operation,literal) {
    let button = event.target;
    const userid = button.dataset.userid;
//    const myObj = {user_id: userid, operation: operation, literal: literal};
//    console.log(myObj);
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
//      .then(() => {
//      updateStatementGGPSubscribing();
//  })

}


function subscribeGGPA(event) {
// Сдесь делаем проверку, если у кнопки есть свойство active - то выполняем функцию   patchSubGGPClasses(event,"add","A");
  console.log('Подписываемся на А')
  patchSubGGPClasses(event,"add","A");
// иначе
//  patchSubGGPClasses(event,"remove","A");
//  console.log('Отписываемся от А')

}
function subscribeGGPB(event) {
  patchSubGGPClasses(event,"add","B");
}

function subscribeGGPC1(event) {
  patchSubGGPClasses(event,"add","C1");
}

// Блок отписок
function unsubscribeGGPA(event) {
  console.log('Отписываемся от А')
  patchSubGGPClasses(event,"remove","A");
}

function unsubscribeGGPB(event) {
  patchSubGGPClasses(event,"remove","B");
}
function unsubscribeGGPC1(event) {
  patchSubGGPClasses(event,"remove","C1");
}

function handleClickFunction(event) {
  event.target.classList.toggle('active');
}



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



// работа с кнопками перекрашивает их при нажании
const elements = document.getElementsByClassName('ggp-classes-sub')


for (let element of elements) {
element.addEventListener('click', handleClickFunction)
}
//

updateStatementGGPSubscribing()

let subA = document.getElementById('ggpA');
let subB = document.getElementById('ggpB');
let subC1 = document.getElementById('ggpC1');

let unsubA = document.getElementById('ggpA');
let unsubB = document.getElementById('ggpB');
let unsubC1 = document.getElementById('ggpC1');

subA.addEventListener('click', subscribeGGPA);
subB.addEventListener('click', subscribeGGPB);
subC1.addEventListener('click', subscribeGGPC1);

unsubA.addEventListener('click', unsubscribeGGPA);
unsubB.addEventListener('click', unsubscribeGGPB);
unsubC1.addEventListener('click', unsubscribeGGPC1);

//медот PATCH запроса




