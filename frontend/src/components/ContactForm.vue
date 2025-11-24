<template>
  <div class="flex justify-center items-center pb-12">
    <div class="w-11/12 max-w-lg pt-16">
      <VForm
        ref="form"
        @submit="onSubmit"
        :validation-schema="schema"
        :initial-values="formValues"
        v-slot="{ errors }"
        @invalid-submit="onInvalidSubmit"
      >
        <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div id="HeaderLogo" class="w-20 mx-auto">
            <img alt="Connect Logo" src="../assets/globe_solid_full.svg" />
          </div>
          <h2 class="font-medium text-center leading-tight text-4xl my-2.5 text-blue">
            Contact Us
          </h2>
          <div class="mb-2.5 text-left">
            <label class="uppercase tracking-wide text-blue text-xs font-bold mb-2">Name</label>
            <VField
              name="name"
              type="text"
              class="w-full bg-white text-charcoal border border-gray-200 rounded py-2 px-3 mb-2 hover:border-blue focus:outline-none focus:ring-1 focus:ring-blue focus:border-transparent"
              :class="{ 'border-red-500': errors.name }"
            />
            <div class="text-red-500 text-xs italic">
              {{ errors.name }}
            </div>
          </div>
          <div class="mb-2.5 text-left">
            <label class="uppercase tracking-wide text-blue text-xs font-bold mb-2">Email</label>
            <VField
              name="email"
              type="text"
              class="w-full bg-white text-charcoal border border-gray-200 rounded py-2 px-3 mb-2 hover:border-blue focus:outline-none focus:ring-1 focus:ring-blue focus:border-transparent"
              :class="{ 'border-red-500': errors.email }"
            />
            <div class="text-red-500 text-xs italic">
              {{ errors.email }}
            </div>
          </div>
          <div class="mb-2.5 text-left">
            <label class="uppercase tracking-wide text-blue text-xs font-bold mb-2"
              >Contact Number
              <VuePopper
                placement="top"
                offsetDistance="4"
                hover
                content="Please enter a valid South African contact number."
                class="normal-case"
              >
                <i class="fa-solid fa-circle-info text-red"></i></VuePopper
            ></label>
            <VField name="contact_number" v-slot="{ field }">
              <vue-tel-input
                v-model="phone"
                defaultCountry="ZA"
                v-bind="field"
                @on-input="phoneChanged"
                class="text-charcoal! border! border-gray-200! rounded! mb-2! hover:border-blue! focus:outline-none! focus:ring-0! focus:border-blue!"
                :class="{ 'border-red-500!': errors.contact_number }"
              ></vue-tel-input>
            </VField>
            <div class="text-red-500! text-xs! italic!">
              {{ errors['contact_number'] }}
            </div>
          </div>
          <div class="mt-4 mb-2.5 text-left">
            <label class="uppercase tracking-wide text-blue text-xs font-bold mb-2">Message</label>
            <VField
              name="message"
              as="textarea"
              rows="3"
              class="w-full bg-white text-charcoal border border-gray-200 rounded py-2 px-3 mb-0.5 hover:border-blue focus:outline-none focus:ring-1 focus:ring-blue focus:border-transparent"
              :class="{ 'border-red-500': errors['message'] }"
            />
            <div class="text-red-500 text-xs italic">
              {{ errors['message'] }}
            </div>
          </div>
          <div class="flex items-center justify-between mt-5">
            <button
              :disabled="isLoading"
              class="w-full bg-blue hover:bg-darkblue text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline cursor-pointer transition-colors"
              type="submit"
            >
              <span v-if="isLoading">
                <i class="fa-solid fa-spinner animate-spin"></i>
                Submitting...
              </span>
              <span v-else>Submit</span>
            </button>
          </div>
        </div>
      </VForm>
    </div>
  </div>
</template>

<script>
import { Form, Field, configure } from 'vee-validate'
import UniDecode from 'unidecode-plus'
import * as Yup from 'yup'
import axios from 'axios'

// Stop contact_number validation on page load.
configure({
  validateOnModelUpdate: false,
})

export default {
  name: 'ContactForm',
  components: {
    VForm: Form,
    VField: Field,
  },
  data() {
    // Declare Yup schema rules for VForm Validation
    const schema = Yup.object().shape({
      name: Yup.string()
        .max(50, 'Name cannot be longer than 50 characters.')
        .test({
          name: 'nameValidation',
          message: "Name may only contain alphabetical characters, '-', '(', ')', '.' and '''",
          test: (value) => this.validateName(value),
        })
        .required('Name is required'),
      email: Yup.string()
        .email('Email must be a valid email address')
        .max(254, 'Email cannot be longer than 254 characters.')
        .required('Email is required'),
      contact_number: Yup.string().test('validPhoneNumber', null, (contact_number) => {
        if (contact_number == '' || contact_number == null) {
          return new Yup.ValidationError('Contact Number is required', null, 'contact_number')
        } else if (contact_number.length != 12) {
          return new Yup.ValidationError(
            'Contact Number cannot be shorter or longer than 10 digits.',
            null,
            'contact_number',
          )
        } else if (contact_number.length == 12) {
          if (this.validateContactNumber(this.phoneObject.number)) {
            this.formValues.contact_number = contact_number
          } else {
            return new Yup.ValidationError(
              'Contact Number is not a valid SA contact number',
              null,
              'contact_number',
            )
          }
          return true
        } else {
          return new Yup.ValidationError('Contact Number is required', null, 'contact_number')
        }
      }),
      message: Yup.string()
        .max(256, 'Message cannot be longer than 256 characters.')
        .required('Message is required'),
    })
    const formValues = {
      name: '',
      email: '',
      contact_number: '',
      message: '',
    }
    return {
      schema,
      formValues,
      phone: '',
      phoneObject: {},
      isLoading: false,
    }
  },
  created() {
    // Set document styling
    document.title = 'Connect - Contact Us'
  },
  mounted() {
    // Set contact_number field styling
    const input = document.getElementsByClassName('vti__input')
    for (let i = 0; i < input.length; i++) {
      input[i].classList.add('placeholder-charcoal!')
      input[i].classList.add('placeholder-charcoal/50!')
      input[i].classList.add('focus:outline-none!')
      input[i].classList.add('focus:ring-0!')
      input[i].classList.add('focus:border-blue!')
      input[i].classList.add('rounded!')
      input[i].classList.add('px-3!')
      input[i].classList.add('py-2!')
    }
    const drop = document.getElementsByClassName('vti__dropdown')
    for (let d = 0; d < drop.length; d++) {
      drop[d].style.borderBottomLeftRadius = '4px'
      drop[d].style.borderTopLeftRadius = '4px'
    }
  },
  methods: {
    // Method to validate name field
    validateName(value) {
      let pattern = /^[-()'. a-zA-Z]+$/
      if (pattern.test(UniDecode(value))) {
        return true
      } else {
        return false
      }
    },
    // Method to validate name field
    validateContactNumber(value) {
      let pattern = /^\+27[1-8][0-9]{8}$/
      if (pattern.test(value)) {
        return true
      } else {
        return false
      }
    },
    // Set contact_number field from vue-tel-input
    phoneChanged(number, phone) {
      this.phoneObject = phone
    },
    // Display success message
    showSuccess() {
      this.$swal(
        'Thank You!',
        'We have received your message and will be in touch shortly!',
        'success',
      )
    },
    // Display error message
    showError() {
      this.$swal({
        icon: 'error',
        title: 'Something went wrong!',
        text: 'Please contact Connect support for assistance',
      })
    },
    // Submit form values to api method
    onSubmit(values, actions) {
      this.isLoading = true
      this.postToAPI(values, actions)
    },
    // Used for development
    onInvalidSubmit({ values, errors, results }) {
      console.log(values) // current form values
      console.log(errors) // a map of field names and their first error message
      console.log(results) // a detailed map of field names and their validation results
    },
    // Api Submit
    postToAPI(values, actions) {
      // Changing phone number object in payload
      values.contact_number = this.phoneObject.number

      // Sending payload to the backend
      axios
        .post('http://127.0.0.1:5175/api/messages/', values)
        .then(() => {
          this.isLoading = false
          // Reset the form and the field values to their initial values
          this.$refs.form.resetForm()
          this.phone = ''
          this.showSuccess()
        })
        .catch((error) => {
          if (
            error.response &&
            error.response.status == '400' &&
            error.response.error == 'Validation failed'
          ) {
            for (let key in error.response.data.details) {
              // Set field errors as they return from backend validation else generic error
              if (Object.prototype.hasOwnProperty.call(this.formValues, key)) {
                let errorMessage = ''
                for (var flatError in error.response.data.details[key]) {
                  errorMessage += error.response.data.details[key][flatError]
                }
                if (key == 'cellphone_number') {
                  this.isLoading = false
                  actions.setFieldError(key, errorMessage)
                } else {
                  this.isLoading = false
                  actions.setFieldError(key, errorMessage)
                }
              } else {
                this.isLoading = false
                this.showError()
              }
            }
            // Log the actual error (in production, use proper logging)
            console.log(error)
          } else {
            this.isLoading = false
            // Log the actual error (in production, use proper logging)
            console.log(error)
            this.showError()
          }
        })
    },
  },
}
</script>

<style scoped>
.vue-tel-input:focus-within {
  -webkit-box-shadow: none !important;
  box-shadow: none !important;
  border-color: #0447e0 !important;
}

:deep(.popper) {
  max-width: 220px;
}

:deep(.popper #arrow::before) {
  background: #ffbb10;
}

:deep(.popper:hover),
:deep(.popper:hover > #arrow::before) {
  background: #ffbb10;
}
</style>
