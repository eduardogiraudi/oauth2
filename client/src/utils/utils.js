async function hash_SHA256(message) {
    const msgBuffer = new TextEncoder().encode(message); 
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);  
    const hashArray = Array.from(new Uint8Array(hashBuffer));  
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');  
    return hashHex;
}
function random_urlsafe (length){
  let result           = '';
  let characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~';

  let charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
     result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
async function generate_code_challenge(code_verifier){
  let hash=await hash_SHA256(code_verifier)
  return btoa(unescape(encodeURIComponent(hash))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function code_verifier_generator(length) {
  if(length<43)length = 43
  if(length>128) length = 128
  return random_urlsafe(length)
 }  
 function random_state_generator(length){
  if(length<43)length = 43
  if(length>128) length = 128
  return random_urlsafe(length)
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
  export {redirect_uri_generator,generate_code_challenge,random_state_generator,random_urlsafe,get_session_storage,set_local_storage,set_session_storage,get_local_storage,set_cookie,get_cookie, code_verifier_generator,hash_SHA256}