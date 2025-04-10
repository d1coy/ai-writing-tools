import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

// Components
import { createApp } from 'vue'
import App from './App.vue'

import router from './router'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App)
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

app.use(router)
app.use(vuetify)
app.use(VueAxios, axios)
app.mount('#app')
