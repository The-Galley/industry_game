import { createStore } from "vuex";

import users from './modules/users';
import games from './modules/games';

export default createStore({
    modules: {
        users,
        games,
    }
});