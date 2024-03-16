document.getElementById('main-form').addEventListener('submit', onSubmit);

const requestURL = `${AppConsts.BaseUrl}/auth/jwt/login`;

async function onSubmit(event) {
  event.preventDefault();

  let el = document.getElementById('main-form');
  let username = el.username.value;
  let password = el.password.value;

  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);


  let response = await fetch(requestURL, {
    method: 'POST',
    headers: {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData.toString()

  });



  if (response.status == 200) {

    alert('Successful Response')
  } else if (response.status == 204) {
    alert('Авторизация прошла успешно')
    window.location = "current_user"

  } else if (response.status == 400) {

    alert('Неверные логин или пароль')

  } else alert('Обратитесь в поддержку')

}


