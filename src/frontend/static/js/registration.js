
document.getElementById('main-form').addEventListener('submit', onSubmit);

// Стрелочная функция, выполняющая проверки правильности введения пароля и повторного
let checkForm = (password, pw2) => {

  let fail = "";

  if (password.length < 3) {
    fail = "Слишком короткий пароль";

  } else if (password.split('&').length > 1) {
    fail = 'Не используйте &';

  } else if (password !== pw2) {
    fail = 'Пароли не совпадают';
  }

  if (fail !== "") {
    document.getElementById('error').innerHTML = fail;
    return false;
  }
  else {
    return true;
  }
};

// объявляем константу с URL-адресом, на котрый будет отправляться запрос
const requestURL = `${AppConsts.BaseUrl}/auth/register`;// 'http://127.0.0.1:8000/auth/register';

// создаём функцию, в которой объявляем переменные, условие и делаем запрос
async function onSubmit(event) {

  //отмена действия браузера, чтобы он ничего не делал, пока юзер на нажмёт на кнопку
  event.preventDefault();

  // объявляю переменные значения которых берутся из HTTP объекта main-form
  let el = document.getElementById('main-form');
  let mail = el.mail.value;
  let password = el.password.value;
  let pw2 = el.repass.value;

  //создаётся переменная чекформрезулт, ей присваиваются результат выполнения ф-и чекформ (тру или фолс)
  // если тру, то создаётся объект бади с данными
  let checkFormResult = checkForm(password, pw2);

  if (checkFormResult) {
    const body = {
      "email": mail,
      "password": password,
    };


    // создаётся ф-я запроса методом FETCH, с Асинхронным запросом
    let response = await fetch(requestURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(body)
    });

    let result = await response.json();
    console.log(JSON.stringify(result));

    // проверка статуса для вывода сообщения о результате выполнения запроса(ошибка или успех)
    if (response.status == 400) {
      alert('Такой пользователь уже существует')


    } else if (response.status == 422) {
      alert('Необходимо использовать почтовый адрес типа xxx@mail.com')

    } else if (response.status == 201) {

      alert('Вы успешно зарегистрировались');
      window.location = "login"
    } else console.log('Что-то пошло нетак, обратитесь в поддержку');

  };
}
