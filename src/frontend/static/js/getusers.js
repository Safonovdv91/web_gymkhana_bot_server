

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
    console.log("Begin")
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

function onSubmitGGPClasses(event) {
  patchSubGGPClasses(event,"add","A");
}

function unsubscribeGGPA(event) {
    event.preventDefault();
    patchSubGGPClasses(event,"remove","A");
  }



//(function sub_A() {
//
//  function onSubmit(event) {
//      patchSubGGPClasses(event,"add","A");
//  }
//  let subA = document.getElementsByClassName('button ggp-classes-sub A-class-button-submit');
//  subA[0].addEventListener('click', onSubmit);
//})();

(function sub_B() {

  function onSubmit(event) {

    event.preventDefault();
    let button = event.target;

    const userid = button.dataset.userid;

    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/subscribe`, {
      method: 'PATCH',
      body: JSON.stringify({
        op: "add",
        sport_class: "B",
      }),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      }
    })
      .then(response => response.json())
      .then(json => console.log(json.details))
  }

  let elements = document.getElementsByClassName('button ggp-classes-sub B-class-button-submit');

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



//// работа с кнопками классов
//let elements = document.getElementsByClassName('ggp-classes-sub');
//const cons = () => {
//  elements.classList.add('active')
//}
//
//for (let element of elements) {
//  element.addEventListener('click', cons);
//}


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


let subA = document.getElementsByClassName('button ggp-classes-sub A-class-button-submit');
let subB = document.getElementsByClassName('button ggp-classes-sub B-class-button-submit');
let subC1 = document.getElementsByClassName('button ggp-classes-sub C1-class-button-submit');

let unsubA = document.getElementsByClassName('patch-button-submit');

subA[0].addEventListener('click', onSubmitGGPClasses);
subB[0].addEventListener('click', onSubmitGGPClasses);
subC1[0].addEventListener('click', onSubmitGGPClasses);

unsubA[0].addEventListener('click', unsubscribeGGPA);

//медот PATCH запроса


//медот PATCH запроса



