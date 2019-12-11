<template>
    <div class="home">
        <img alt="Vue logo" src="../assets/logo.png" />
        <HelloWorld msg="Welcome to Your Vue.js App" />
        <a
            href="https://github.com/login/oauth/authorize?client_id=9f2b73ec45669162ea53&redirect_uri=http://localhost:8080/"
        >Login with Github</a>
    </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
    name: "home",
    components: {
        HelloWorld
    }
};
</script>
