import { auth_api } from "@services/interceptors";
import { auth_server } from "@root/config";
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
  async function start_oauth_flow(){
    const currentUrl = window.location.href;
    const url = new URL(currentUrl);
    if (url.searchParams.has('code')&& get_session_storage('code_verifier')){
      //siamo nell'ultimo step (di scambio di token con il code)
      const code_verifier = get_session_storage('code_verifier')
      sessionStorage.removeItem('code_verifier')
      const auth_code = url.searchParams.get('code');
      const given_state = url.searchParams.get('state')
      const saved_state = get_session_storage('state')
      sessionStorage.removeItem('state')
      url.searchParams.delete('state')
      url.searchParams.delete('code');
      window.history.replaceState({}, document.title, url.toString());
      const redirect_uri=`${url.origin}${url.pathname}`; 
      if(given_state === saved_state){
        auth_api.post('/token',JSON.stringify({
          'code_verifier': code_verifier,
          'code': auth_code,
          'redirect_uri': redirect_uri,
          'client_id': import.meta.env.VITE_CLIENT_ID,
          'state': given_state
        })).then(res=>{
          if(res.status===200){
            set_cookie('token',res.data.message.token)
            set_cookie('refresh_token',res.data.message.refresh_token)
          }else{
            // da fare
          }
          
        })
      }else{
        //errore possibile crfr 
      }
      
    }else{
      const redirect_uri = encodeURIComponent(`${window.location.origin}${window.location.pathname}`);
      const code_verifier =code_verifier_generator(128)
      const code_challenge = generate_code_challenge(code_verifier)
      const state = random_state_generator(64)
      const client_id = import.meta.env.VITE_CLIENT_ID
      set_session_storage('code_verifier', code_verifier);
      set_session_storage('state', state);
      window.location.href = `${auth_server}?response_type=code&client_id=${client_id}&redirect_uri=${redirect_uri}&code_challenge_method=s256&code_challenge=${code_challenge}&state=${state}`
       
      
    }
  }
  export {start_oauth_flow,redirect_uri_generator,generate_code_challenge,random_state_generator,random_urlsafe,get_session_storage,set_local_storage,set_session_storage,get_local_storage,set_cookie,get_cookie, code_verifier_generator,hash_SHA256}