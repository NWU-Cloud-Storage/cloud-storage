<template>
  <el-container style="height: 500px; border: 1px solid #eee">
    <el-header>
      <Header></Header>
    </el-header>
    <el-container direction="horizontal">
      <el-aside>
        <div id="nav">
          <el-menu>
            <router-link to="/">
              <el-menu-item>Home</el-menu-item>
            </router-link>

            <router-link to="/about">
              <el-menu-item>About</el-menu-item>
            </router-link>

            <router-link to="/hello">
              <el-menu-item>Hello World</el-menu-item>
            </router-link>

            <router-link to="/file/">
              <el-menu-item>File</el-menu-item>
            </router-link>
          </el-menu>
        </div>
      </el-aside>
      <el-main>
        <div id="app">
          <router-view></router-view>
        </div>
      </el-main>
    </el-container>

    <el-footer>All rights reserved</el-footer>
  </el-container>
</template>

<script>
  import Header from '@/components/Header.vue'

  export default {
    name: 'app',
    components: {
      Header
    }
  }
</script>

<style>
#app {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
