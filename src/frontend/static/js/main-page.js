

let response = fetch('http://127.0.0.1:9000/api/v1/users/ALL_INFO',  {
    method: 'GET',
    credentials: 'include',
  })
    .then(response => {
      return response.json()
      })
      .then(json => console.log(json))
      .catch(error => console.log(error))

