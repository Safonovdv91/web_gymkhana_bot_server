

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
})();
/*
function handleFormSubmit(event) {
  // Просим форму не отправлять данные самостоятельно
  event.preventDefault()
  console.log('Отправка!')
}

const applicantForm = document.getElementsByClassName('user');
applicantForm.addEventListener('submit', handleFormSubmit);
*/