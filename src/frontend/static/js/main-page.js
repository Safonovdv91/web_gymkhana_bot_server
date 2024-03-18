

const requestURL = 'http://127.0.0.1:9000/api/v1/users';

// блок кода для выпадающих меню
function myFunction() {
  document.getElementById("myDropDown").classList.toggle("show");
}

function myFunction2() {
  document.getElementById("myDropDown2").classList.toggle("show");
}

function myFunction3() {
  document.getElementById("myDropDown3").classList.toggle("show");
}

// Закройте выпадающее меню, если пользователь щелкает за его пределами
window.onclick = function (event) {
  if (!event.target.matches('.hi__listDropBth')) {
    var dropdowns = document.getElementsByClassName("drop__content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  } else if (!event.target.matches('.hi__listDropBth2')) {
    var dropdowns = document.getElementsByClassName("drop__content2");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  } else if (!event.target.matches('.hi__listDropBth3')) {
    var dropdowns = document.getElementsByClassName("drop__content3");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  } else (alert("всё поломалось"))
}



fetch('http://127.0.0.1:9000/api/v1/users/current', {
  method: 'GET',
  credentials: 'include',
})
  .then(response => {
    console.log(response)
    return response.json()
  })
  .then(json => console.log(json))
  .catch(error => console.log(error))



