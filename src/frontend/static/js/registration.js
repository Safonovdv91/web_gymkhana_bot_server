
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
const requestURL = 'http://127.0.0.1:9000/auth/register';

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
    if (response.status == 400 ) {
      //const str = JSON.stringify(result);
      //const arr = JSON.parse(str);
      //alert(arr.detail);
      alert('Такой пользователь уже существует')


    } else if (response.status == 422) {
      //const str = JSON.stringify(result);
      //const arr = JSON.parse(str);
      //alert(arr.detail[0].msg);
      alert('Необходимо использовать почтовый адрес типа xxx@mail.com')

    } else if (response.status == 201) {

        alert('Вы успешно зарегистрировались');
        window.location = "authorization.html"
    } else console.log('Что-то пошло нетак, обратитесь в поддержку');

  };
}


/*
// функция, которая создаёт метод запроса, в данном случае это метод XML HTTP Request

function sendRequest(method, url, body = null) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.open(method, url)

    xhr.responseType = 'json'
    xhr.setRequestHeader('Content-Type', 'application/json')

    xhr.onload = () => {
      if (xhr.status >= 400) {
        reject(xhr.response)
      } else {
        resolve(xhr.response);
      }
    }

    xhr.onerror = () => {
      reject(xhr.response)
    }

    xhr.send(JSON.stringify(body))
  })
};

    //отправляется пост-запрос и метод запроса, при правильном выполнении которого будет редирект на логин страницу
    // или алерт с описанием ошибки

   /* sendRequest('POST', requestURL, body)
      .then(data => {
        console.log(data);
        window.location = "login.html"
      })
      .catch(err => {


        console.log(err);



        const str = JSON.stringify(err);

        const arr = JSON.parse(str);

        alert(arr.detail[0].msg);

      })*/
