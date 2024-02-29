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
  setUser(state, token) {
    const parsedData = parseJwt(token);
    state.user = {
      token: token,
      id: parsedData.id,
      username: parsedData.username,
      type: parsedData.type,
    };
  },
  logout(state, user){
    state.user = user;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};

function parseJwt (token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(window.atob(base64).split('')
.map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  })
.join(''));
  return JSON.parse(jsonPayload);
}