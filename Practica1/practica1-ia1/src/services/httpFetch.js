const postData = async (endpoint = "", data = {}) => {
  // Opciones por defecto estan marcadas con un *
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify(data);

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
    timeout: 180000, // 3 minutos
  };

  return fetch(`http://127.0.0.1:5000${endpoint}`, requestOptions);
};

export default postData;
