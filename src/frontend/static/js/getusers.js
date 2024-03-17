

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

    let button = event.target;

    const userid = button.dataset.userid;

    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/subscribe`, {
      method: 'PATCH',
      body: JSON.stringify({
        op: "add",
        sport_class: "C1",
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


