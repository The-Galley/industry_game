import axios from 'axios';


const state = {
  user: null,
};

const url = 'https://industry-game.ru';

const getters = {
  isAuthenticated: state => !!state.user,
  isAdmin: state => state?.user?.type === 'ADMIN',
  isPlayer: state => state?.user?.type === 'PLAYER',
  stateUser: state => state.user,
};

const actions = {
  async checkAuth({ commit }) {
    const token = getCookie('token');
      try {
        const userData = await getUserData(token);
        console.log(userData.token);
        commit('setUser', userData);
      } catch (error) {
        console.error('Error checking authentication:', error);
      }
  },
  async register({dispatch}, user) {
    let {data} = await axios.post(url + '/api/v1/players/register/', user);
    await dispatch('saveMe', data);
  },
  async login({dispatch}, user) {
    let {data} = await axios.post(url + '/api/v1/players/login/', user);
    await dispatch('saveMe', data);
  },
  async saveMe({commit}, data) {
    document.cookie = `token=${data.token}; path=/;`;
    await commit('setUser', data.token);
  },
  async logOut({commit}) {
    let user = null;
    commit('logout', user);
  }
};

const mutations = {
  setUser(state, userData) {
    state.user = userData;
  },
  logout(state, user) {
    state.user = user;
  },
};

async function getUserData(token) {
  const parsedData = parseJwt(token);
  return {
    token: token,
    id: parsedData.id,
    username: parsedData.username,
    type: parsedData.type,
  };
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';')
.shift();
}

export default {
  state,
  getters,
  actions,
  mutations
};

function parseJwt (token) {
  let base64Url = token.split('.')[1];
  let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  let jsonPayload = decodeURIComponent(window.atob(base64).split('')
.map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  })
.join(''));
  return JSON.parse(jsonPayload);
}