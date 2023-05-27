import axios from "axios";

class AdminConsole {
  api_get = async (url) => {
    const res = await axios.get(url);
    if (res.status === 200) {
      return res.data;
    } else {
      console.log('API-GET', res);
      return false
    }
  }

  api_post = async (url, data) => {
    const res = await axios.post(url, data);
    if (res.status === 200) {
      return res.data;
    } else {
      console.log('API-POST', res);
      return false
    }
  }

  api_put = async (url, data) => {
    const res = await axios.put(url, data);
    if (res.status === 200) {
      return res.data;
    } else {
      console.log('API-PUT', res);
      return false
    }
  }

  grant_perms = async (user_id, perm_id) => {
    return await this.api_post(`/grant_perms`, { username: user_id, perm: perm_id });
  }
  
  revoke_perms = async (user_id, perm_id) => {
    return await this.api_post(`/revoke_perms`, { username: user_id, perm: perm_id });
  }
  
  check_perms = async (user_id) => {
    return await this.api_post(`/check_permissons`, { username: user_id });
  }
}

export default AdminConsole;