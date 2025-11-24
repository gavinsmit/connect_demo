import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

//Tailwind CSS
import './index.css'

//Vue tel input
import VueTelInput from 'vue-tel-input'
import 'vue-tel-input/dist/vue-tel-input.css'

//Vue 3 popper
import Popper from 'vue3-popper'
import './assets/popper.css'

//Vue sweetalert
import VueSweetalert2 from 'vue-sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

const globalOptions = {
  mode: 'national',
  dropdownOptions: {
    disabled: true,
  },
  inputOptions: {
    placeholder: 'Enter a contact number',
  },
}

const options = {
  color: '#3c3c3d',
  confirmButtonColor: '#08486f',
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueTelInput, globalOptions)
app.component('VuePopper', Popper)
app.use(VueSweetalert2, options)

app.mount('#app')
