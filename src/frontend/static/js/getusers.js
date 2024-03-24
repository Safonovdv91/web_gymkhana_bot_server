var rmg = rmg || {};

(function () {

  // Метод обновления свечения буковки подписки класса.
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
            //console.log(classLetter.sport_class);
            if (ggpClass.textContent == classLetter.sport_class) {
              ggpClass.classList.add('active');
            }
          })
        }
      }
    }
  }

  // функция получения статуса чекбокса при загрузке страницы

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
    let content = document.getElementById('class-buttons')

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

  // функции патч-запроса при нажатии на чек-бокс
  // на GGP
  function patchSub_GGP(event, sub_ggp_on) {
    let button = event.target;
    const userid = button.dataset.userid;
    console.log(userid);

    fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/patch`, {
      method: 'PATCH',
      body: JSON.stringify({
        sub_ggp: sub_ggp_on,
      }),
      headers: {
        'Content-Type': 'application/json; charset=UTF-8'
      }
    }).then(response => response.json())
      .then(json => console.log(json.data));
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

  // переключатели чекбоксов
  function onToggleSub_GGP(event) {
    event.target.classList.toggle('active');

    if (event.target.getAttribute('class').includes('active')) {
      patchSub_GGP(event, 'true');
    } else {
      patchSub_GGP(event, 'false');
    }
  }

  // Кнопка разлогиниться
  async function onExit(event) {

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

    } else console.log('Что-то пошло нетак, обратитесь в поддержку');
  };

  // Добавляем обработчики событий.
  function addEventListeners() {
    // Сворачивание кнопок классов
    let collapseButtons = document.getElementsByClassName('collapse');
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

    const toggleButton_GGP = document.getElementById('checkbox-iosGGP')
    toggleButton_GGP.addEventListener('click', onToggleSub_GGP);

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

// блок патч-запроса подписки на проценты

// слушатель нажатия на чекбокс
const toggleButton_percent = document.getElementById('checkbox-iosPercent')
toggleButton_percent.addEventListener('click', onToggleSub_percent);

// функция инициирующая запрос
function onToggleSub_percent(event) {
  event.target.classList.toggle('active');

  if (event.target.getAttribute('class').includes('active')) {
    patchSub_percent(event, 'true');
  } else {
    patchSub_percent(event, 'false');
  }
}

// патч запрос на сервер для вкл/выкл подписки на проценты
function patchSub_percent(event, percent_on) {
  let button = event.target;
  const userid = button.dataset.userid;

  fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/patch`, {
    method: 'PATCH',
    body: JSON.stringify({
      sub_ggp_percent: percent_on,
    }),
    headers: {
      'Content-Type': 'application/json; charset=UTF-8'
    }
  }).then(response => response.json())
    .then(json => console.log(json.data));
}

// блок патч-запроса подписки на оффлайн
// слушатель нажатия на чекбокс
const toggleButton_offline = document.getElementById('checkbox-iosOffline')
toggleButton_offline.addEventListener('click', onToggleSub_offline);

// функция инициирующая запрос
function onToggleSub_offline(event) {
  event.target.classList.toggle('active');

  if (event.target.getAttribute('class').includes('active')) {
    patchSub_offline(event, 'true');
  } else {
    patchSub_offline(event, 'false');
  }
}

// патч запрос на сервер для вкл/выкл подписки на проценты
function patchSub_offline(event, offline_on) {
  let button = event.target;
  const userid = button.dataset.userid;

  fetch(`${AppConsts.BaseUrl}/api/v1/users/id=${userid}/patch`, {
    method: 'PATCH',
    body: JSON.stringify({
      sub_offline: offline_on,
    }),
    headers: {
      'Content-Type': 'application/json; charset=UTF-8'
    }
  }).then(response => response.json())
    .then(json => console.log(json.data));
}

// блок модального окна

const btns = document.querySelectorAll('.btn');
const modalOverlay = document.querySelector('.modal-overlay')
const modals = document.querySelector('.modal')

btns.forEach((el) => {
  el.addEventListener('click', (e) => {
    let path = e.currentTarget.getAttribute('data-path');

    document.querySelector(`[data-target="${path}"]`).classList.add('modal-visible')
    modalOverlay.classList.add('modal-overlay-visible');
  });
});

// выход из модального окна по клику в пустоту
modalOverlay.addEventListener('click', (e) => {

  if (e.target == modalOverlay) {
    modalOverlay.classList.remove('modal-overlay-visible');
  };
});

// выход из модального окна по нажатию на эскейп
document.addEventListener('keydown', (event) => {

  if (event.which === 27) {
    modalOverlay.classList.remove('modal-overlay-visible');
  }
});
