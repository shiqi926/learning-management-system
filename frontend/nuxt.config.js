export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'spm',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: '~/plugins/vuex-persist.js', ssr: false },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/buefy
    'nuxt-buefy',
    '@nuxtjs/axios'
  ],

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    extend(config) {
      config.resolve.alias['vue'] = 'vue/dist/vue.common'
    }
  },
  
  axios: {
    // proxy: true
  },

  target: 'static',

  generate: {
    fallback: true
    // routes: function() {
    //   let coursePoints = axios.get("https://spmg7-backend.herokuapp.com/api/courses/")
    //   .then((res) => {
    //     return res.data.map((course) => {
    //       return "/course/" + course.id
    //     })
    //   });
    //   let 
    // }
  }
}
