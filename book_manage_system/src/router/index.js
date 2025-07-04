import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: () => import("@/components/Login.vue") },
  { path: "/register", component: () => import("@/components/Register.vue") },
  {
    path: "/loginmanage",
    component: () => import("@/components/BookManage/LoginBookManage.vue"),
  },
  {
    path: "/home",
    component: () => import("@/components/Home/Home.vue"),
    redirect: "/index",
    children: [
      {
        path: "/index",
        component: () => import("@/components/Index/Index.vue"),
        meta: {
          title: "首页",
        },
      },
      {
        path: "/search",
        component: () => import("@/components/User/Search.vue"),
      },
      { path: "/rule", component: () => import("@/components/User/Rule.vue") },
      {
        path: "/notice",
        component: () => import("@/components/User/Notice.vue"),
      },
      {
        path: "/information",
        component: () => import("@/components/User/Information.vue"),
      },
      {
        path: "/borrow",
        component: () => import("@/components/User/Borrow.vue"),
      },
      {
        path: "/violation",
        component: () => import("@/components/User/Violation.vue"),
      },
      {
        path: "/comment",
        component: () => import("@/components/User/Comment.vue"),
      },
      {
        path: "/intelligent",
        component: () => import("@/components/User/Intelligent.vue"),
      },
      // { path: "/chat", component: () => import("@/components/User/Chat") },
    ],
  },
  {
    path: "/homemange",
    component: () => import("@/components/Home/HomeManage.vue"),
    children: [
      {
        path: "/borrowbook",
        component: () => import("@/components/BookManage/BorrowBook.vue"),
      },
      {
        path: "/returnbook",
        component: () => import("@/components/BookManage/ReturnBook.vue"),
      },
      {
        path: "/borrowstatement",
        component: () => import("@/components/BookManage/BorrowStatement.vue"),
      },
      {
        path: "/returnstatement",
        component: () => import("@/components/BookManage/ReturnStatement.vue"),
      },
      {
        path: "/noticemanage",
        component: () => import("@/components/BookManage/NoticeManage.vue"),
      },
      {
        path: "/bookexpire",
        name: "bookexpire",
        component: () => import("@/components/BookManage/BookExpire.vue"),
      },
    ],
  },
  {
    path: "/loginadmin",
    component: () => import("@/components/Admin/LoginAdmin.vue"),
  },
  {
    path: "/homeadmin",
    component: () => import("@/components/Home/HomeAdmin.vue"),
    children: [
      {
        path: "/bookmanage",
        component: () => import("@/components/Admin/BookManage.vue"),
      },
      {
        path: "/booktype",
        component: () => import("@/components/Admin/BookType.vue"),
      },
      {
        path: "/statementmanage",
        component: () => import("@/components/Admin/StatementManage.vue"),
      },
      {
        path: "/statementsearch",
        component: () => import("@/components/Admin/StatementSearch.vue"),
      },
      {
        path: "/statementrulemanage",
        component: () => import("@/components/Admin/StatementRuleManage.vue"),
      },
      {
        path: "/bookadminmanage",
        component: () => import("@/components/Admin/BookAdminManage.vue"),
      },
      {
        path: "/adminmanage",
        component: () => import("@/components/Admin/AdminManage.vue"),
      },
      {
        path: "/intelligent_analysis",
        component: () => import("@/components/Admin/IntelligentAnalysis.vue"),
      },
    ],
  },
  {
    path: "/404",
    component: () => import("@/components/404/404.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/404",
  },
];

const router = new VueRouter({
  routes,
});
// 白名单路径（无需登录即可访问）
const whiteList = ['/login', '/loginmanage', '/loginadmin', '/register'];

router.beforeEach((to, from, next) => {
  const tokenStr = window.sessionStorage.getItem("token");

  if (tokenStr) {
    // 已登录，放行所有页面
    next();
  } else {
    if (whiteList.includes(to.path)) {
      // 放行白名单页面
      next();
    } else {
      // 非白名单页面 → 强制跳转登录页
      next('/login');
    }
  }
});

export default router
