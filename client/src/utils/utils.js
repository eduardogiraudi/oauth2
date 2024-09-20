async function hash_SHA256(message) {
    const msgBuffer = new TextEncoder().encode(message); 
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);  
    const hashArray = Array.from(new Uint8Array(hashBuffer));  
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');  
    return hashHex;
}

 function code_verifier_generator(length) {
    let result           = '';
    let characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    if(length<43){
        length = 43
    }
    let charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
       result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
 }
  const get_cookie = (name) => {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [cookieName, cookieValue] = cookie.trim().split('=');
      if (cookieName === name) {
        return cookieValue;
      }
    }
    return null;
  };
   function set_cookie (name, value)  {
    document.cookie = `${name}=${value}`;
  }
   function set_local_storage (name, value) {
    localStorage.setItem(name,JSON.stringify(value))
  }
   function get_local_storage (name) {
    return JSON.parse(localStorage.getItem(name))
  }
   function set_session_storage (name, value) {
    sessionStorage.setItem(name,JSON.stringify(value))
  }
   function get_session_storage (name) {
    return JSON.parse(sessionStorage.getItem(name))
  }
   function redirect_uri_generator(){
    return window.location.href
  }
  export {redirect_uri_generator,get_session_storage,set_local_storage,set_session_storage,get_local_storage,set_cookie,get_cookie, code_verifier_generator,hash_SHA256}