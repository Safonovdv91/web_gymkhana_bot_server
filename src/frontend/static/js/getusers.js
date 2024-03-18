var rmg = rmg || {};

(function () {

  // Метод обновления состояния буковки подписки класса.
  function updateSubGGPClasses(user) {
    let userId = user.id;
    let formUsers = document.getElementsByClassName('user');
    // перебор html форм class="user"
    for (let formUser of formUsers) {
      let formId = formUser.getAttribute('data-userid');
      if (userId == formId) {
        let ggpClasses = formUser.getElementsByClassName('ggp-classes-sub');
        for (let ggpClass of ggpClasses) {
          console.log(ggpClass.textContent);
          user.ggp_sub_classes.forEach(classLetter => {
            console.log(classLetter.sport_class);
            if (ggpClass.textContent == classLetter.sport_class) {
              ggpClass.classList.add('active');
            }
          })
        }
      }
    }
  }

  // Получить пользователей.
  function getUsers() {
    console.log('Обновляем данные о GGP');
    fetch(`${AppConsts.BaseUrl}/api/v1/users`, {
      method: 'GET',
      credentials: 'include',
    }).then(response => {
      return response.json();
    }).then(json => {
      json.data.forEach(user => {
        updateSubGGPClasses(user);
      });
    }).catch(error => console.log(error));
  }

  // Удалить пользователя.
  function onDelete(event) {
    event.preventDefault();
    console.log('Отправка!')

    let button = event.target;
    let userid = button.dataset.userid;

    // метод DELETE запроса - это переделать
    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/delete`, {
      method: 'DELETE'
    }).then(response => response.json())
      .then(json => console.log(json));
  }

  // Свернуть/Развернуть классы спортсменов.
  function onCollapse(event) {
    event.preventDefault();
    console.log('click');

    this.classList.toggle('active');
    let content = this.nextElementSibling;

    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + 'px';
    }
  }

  // Функция подписки на классы в соответствии с логикой.
  function patchSubGGPClasses(event, operation, literal) {
    let button = event.target;
    const userid = button.dataset.userid;

    //медот PATCH запроса
    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/subscribe`, {
      method: 'PATCH',
      body: JSON.stringify({
        op: operation,
        sport_class: literal,
      }),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      }
    }).then(response => response.json())
      .then(json => console.log(json.details));
  }

  // Переключатель свечения кнопки и выбора метода.
  function onToggleSubGGpClasses(event) {
    event.target.classList.toggle('active');

    if (event.target.getAttribute('class').includes('active')) {
      patchSubGGPClasses(event, 'add', event.target.innerText);
    } else {
      patchSubGGPClasses(event, 'remove', event.target.innerText);
    }
  }

  // Создаём функцию, в которой объявляем переменные, условие и делаем запрос
  async function onExit(event) {
    // отмена действия браузера, чтобы он ничего не делал, пока юзер на нажмёт на кнопку
    event.preventDefault();

    // объявляем константу с URL-адресом, на котрый будет отправляться запрос
    const requestLogoutURL = `${AppConsts.BaseUrl}/auth/jwt/logout`;

    // создаётся ф-я запроса методом FETCH, с Асинхронным запросом
    let response = await fetch(requestLogoutURL, {
      method: 'POST',
      headers: {
        'Accept': 'application/json'
      },
      body: JSON.stringify({})
    });

    // проверка статуса для вывода сообщения о результате выполнения запроса(ошибка или успех)
    if (response.status == 200 || response.status == 204) {
      alert('Success');
      window.location = "login";
    } else if (response.status == 401) {
      alert('Inactive user');
      window.location = "login";

    } else console.log('Что-то пошло нетак, обратитесь в поддержку');
  };

  // Добавляем обработчики событий.
  function addEventListeners() {
    // Сворачивание кнопок классов
    let collapseButtons = document.getElementsByClassName('collaps');
    for (let collapseButton of collapseButtons) {
      collapseButton.addEventListener('click', onCollapse);
    }

    let deleteButtons = document.getElementsByClassName('delete-button-submit');
    for (let deleteButton of deleteButtons) {
      deleteButton.addEventListener('click', onDelete);
    }

    const toggleButtons = document.getElementsByClassName('ggp-classes-sub')

    for (let toggleButton of toggleButtons) {
      toggleButton.addEventListener('click', onToggleSubGGpClasses);
    }

    const exitButton = document.getElementById('patch-button-exit');
    exitButton.addEventListener('click', onExit);
  }

  function init() {
    addEventListeners();
    getUsers();
  }

  // Инициализируем rmg.users.
  init();
})();
