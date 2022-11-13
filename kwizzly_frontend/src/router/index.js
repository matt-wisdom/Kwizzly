import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // {
  //   path: '/admin-page',
  //   name: 'admin',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AdminView.vue')
  // },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/create-quiz',
    name: 'create-quiz',
    component: () => import('../views/CreateQuiz.vue')
  },
  {
    path: "/quizes",
    name: "quizes",
    component: () => import('../views/QuizesView.vue')
  },
  {
    path: "/view-quiz/:id",
    name: "view-quiz",
    component: () => import('../views/ViewQuiz.vue')
  },
  {
    path: "/private-quizes",
    name: "private-quizes",
    component: () => import('../views/PrivateQuizes.vue')
  },
  {
    path: "/my-profile",
    name: "my-profile",
    component: () => import('../views/MyProfile.vue')
  },
  {
    path: "/leaderboard/:quiz_id",
    name: "leaderboard",
    component: () => import('../views/LeaderBoard.vue')
  },
  {
    path: "/play-single/:quiz_id",
    name: "play-single",
    component: () => import('../views/PlaySingle.vue')
  },
  {
    path: "/play-multi/:quiz_id",
    name: "play-multi",
    component: () => import('../views/PlayMulti.vue')
  },
  {
    path: "/join-multi/:gameid",
    name: "join-multi",
    component: () => import('../views/JoinMulti.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  if (to.name === "login" || to.name === "register" || to.name === "home" || to.name === "quizes"){
    return true
  }
  if (localStorage.getItem("access_token")){
    return true
  }
  return {name: "login", query: {"next": to.path}}
})

export default router
