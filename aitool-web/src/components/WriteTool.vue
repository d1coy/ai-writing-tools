<script setup lang="ts">
  import axios from 'axios'
  import { ref } from 'vue'

  const VITE_BASE_URL = import.meta.env.VITE_BASE_URL
  const VITE_ENV = import.meta.env.VITE_ENV
  const apiPrefix = VITE_ENV === 'prod' ? '' : '/api'
  const baseURL = VITE_BASE_URL || ''
  const apiClient = axios.create({
     baseURL: baseURL,
  })

  const selectedLanguage = ref('English')
  const languages = ref([
    'English', 'Simplified Chinese', 'Traditional Chinese', 'Cantonese', 'Japanese', 'Korean',
    'Spanish', 'French', 'German', 'Italian', 'Arabic', 'Russian', 'Dutch', 'Portuguese', 'Bengali',
    'Indonesian', 'Urdu', 'Hindi', 'Swahili', 'Marathi', 'Telugu', 'Turkish', 'Tamil', 'Vietnamese',
    'Persian (Farsi)', 'Gujarati', 'Polish', 'Ukrainian', 'Malayalam', 'Kannada', 'Thai', 'Burmese',
    'Punjabi', 'Romanian', 'Javanese', 'Hausa', 'Filipino (Tagalog)', 'Yoruba', 'Sindhi', 'Uzbek',
    'Amharic', 'Azerbaijani', 'Kurdish', 'Oriya (Odia)', 'Maithili', 'Malay', 'Nepali', 'Sinhala',
    'Khmer', 'Somali', 'Zulu',
  ])
  const selectedTone = ref('Professional')
  const toneList = ref([
    'Professional', 'Academic', 'Friendly', 'Casual', 'Business',
    'Creative', 'Persuasive', 'Journalistic', 'Poetic', 'Storytelling',
  ])
  const selectedLength = ref(50)
  const selectedLengthMode = ref('Expand')
  const lengthModeList = ref(['Expand', 'Extract'])
  const formatFile = ref([])
  const roleFile = ref([])
  const fileRules = ref([
    (file: any) => {
      if (file !== undefined && (!file.name.endsWith('.txt') || file.type !== 'text/plain')) {
        error('Only accept txt file')
        if (mode.value === 'format') {
          formatFile.value = []
        }
        if (mode.value === 'role') {
          roleFile.value = []
        }
      }
      return true
    }
  ])
  
  const inputText = ref('')
  const outputText = ref('')
  const mode = ref('tone')
  const snackbarMsg = ref('')
  const showSnackbarTop = ref(false)

  function process() {
    if (inputText.value.trim() === '' && mode.value !== 'format') {
      error('Input text cannot be empty')
      return
    }
    if (mode.value === 'format') {
      if (!formatFile.value || formatFile.value.length === 0) {
        error('Input file cannot be empty')
        return
      }
    }
    if (mode.value === 'role') {
      if (!roleFile.value || roleFile.value.length === 0) {
        error('Input file cannot be empty')
        return
      }
    }
    if (mode.value === 'translate') {
      apiClient.post(apiPrefix + '/translate', {
        content: inputText.value,
        target_lang: selectedLanguage.value,
      })
      .then((res) => {
        if (res.data.success) {
          outputText.value = res.data.data
        } else {
          console.log(res.data.message)
          error(res.data.message)
        }
      })
      .catch((e) => {
        console.log(e)
      })
    } else if (mode.value === 'tone') {
      apiClient.post(apiPrefix + '/tone', {
        text: inputText.value,
        style: selectedTone.value.toLowerCase(),
      })
      .then((res) => {
        if (res.data.success) {
          outputText.value = res.data.data
        } else {
          console.log(res.data.message)
          error(res.data.message)
        }
      })
      .catch((e) => {
        console.log(e)
      })
    } else if (mode.value === 'length') {
      apiClient.post(apiPrefix + '/process-text', {
        prompt: inputText.value,
        mode: selectedLengthMode.value.toLowerCase(),
        max_word: selectedLength.value,
      })
      .then((res) => {
        if (res.data.success) {
          outputText.value = res.data.data
        } else {
          console.log(res.data.message)
          error(res.data.message)
        }
      })
      .catch((e) => {
        console.log(e)
      })
    } else if (mode.value === 'summary') {
      apiClient.post(apiPrefix + '/summary', {
        prompt: inputText.value,
      })
      .then((res) => {
        if (res.data.success) {
          outputText.value = res.data.data
        } else {
          console.log(res.data.message)
          error(res.data.message)
        }
      })
      .catch((e) => {
        console.log(e)
      })
    } else if (mode.value === 'format') {
      const formData = new FormData()
      // @ts-ignore
      formData.append('file', formatFile.value)
      apiClient.post(apiPrefix + '/format-text', formData, {
        responseType: 'blob'
      })
      .then((res) => {
        if (res.status === 200) {
          if (res.headers['content-type'] === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
            download(res.data, res.headers['content-disposition'].match(/filename=(.+)/)[1])
          } else {
            if (!res.data.success) {
              console.log(res.data.message)
              error(res.data.message)
            }
          }
        }
      })
      .catch((e) => {
        console.log(e)
      })
    } else if (mode.value === 'role') {
      const formData = new FormData()
      // @ts-ignore
      formData.append('file', roleFile.value)
      formData.append('content', inputText.value)
      apiClient.post(apiPrefix + '/role', 
        formData
      )
      .then((res) => {
        if (res.data.success) {
          outputText.value = res.data.data
        } else {
          console.log(res.data.message)
          error(res.data.message)
        }
      })
      .catch((e) => {
        console.log(e)
      })
    }
  }

  function download(data: Blob, filename: string) {
    const a = document.createElement('a')
    const url = window.URL || window.webkitURL
    console.log('URL\n')
    console.log(url)
    const herf = url.createObjectURL(data)
    console.log('herf\n')
    console.log(herf)
    a.href = herf
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(herf)
  }

  function reset() {
    if (mode.value === 'format') {
      formatFile.value = []
      return
    }
    inputText.value = ''
    outputText.value = ''
  }

  function error(msg: string) {
    showSnackbarTop.value = true
    snackbarMsg.value = msg
  }

</script>

<template>
  <v-snackbar v-model="showSnackbarTop" :timeout="2000" location="top" color="error">
    {{ snackbarMsg }}
  </v-snackbar>
  <div class="item">
    <v-btn @click="mode = 'tone'" :color="mode === 'tone' ? 'primary' : 'default'">
      Change Tone
    </v-btn>
    <v-btn @click="mode = 'length'" :color="mode === 'length' ? 'primary' : 'default'">
      Adjust Length
    </v-btn>
    <v-btn @click="mode = 'summary'" :color="mode === 'summary' ? 'primary' : 'default'">
      Summary
    </v-btn>
    <v-btn @click="mode = 'format'" :color="mode === 'format' ? 'primary' : 'default'" prepend-icon="mdi-note-text-outline">
      Format
    </v-btn>
    <v-btn @click="mode = 'role'" :color="mode === 'role' ? 'primary' : 'default'" prepend-icon="mdi-emoticon-outline">
      Customize Role
    </v-btn>
    <v-dialog width="auto" scrollable>
      <template #activator="{ props: activatorProps }">
        <v-btn prepend-icon="mdi-earth" v-bind="activatorProps" text="Translate" @click="mode = 'translate'" 
              :color="mode === 'translate' ? 'primary' : 'default'"
        ></v-btn>
      </template>
      <template #default="{ isActive }">
        <v-card prepend-icon="mdi-earth" title="Select Language">
          <v-divider class="mt-3"></v-divider>
          <v-card-text class="px-4" style="height: 300px">
            <v-radio-group v-model="selectedLanguage" messages="Select a Language from the radio group">
              <v-radio v-for="lang in languages" :key="lang" :label="lang" :value="lang"></v-radio>
            </v-radio-group>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn text="Close" @click="isActive.value = false"></v-btn>
            <v-spacer></v-spacer>
            <v-btn color="surface-variant" text="OK" variant="flat" @click="isActive.value = false; mode = 'translate'"></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
    <v-select class="mt-1" bg-color="white" label="Tone" :items="toneList" v-model="selectedTone" v-if="mode === 'tone'"></v-select>
    <v-row v-if="mode === 'length'">
      <v-col span="12">
        <v-select bg-color="white" label="Mode" :items="lengthModeList" v-model="selectedLengthMode" class="mt-1"></v-select>
      </v-col>
      <v-col span="12">
        <v-number-input :reverse="false" controlVariant="default" label="Length" :hideInput="false" 
                      :inset="false" :min="10" :max="500" v-model="selectedLength" bg-color="white" class="mt-1"
        ></v-number-input>
      </v-col>
    </v-row>
    <template v-if="mode === 'format'">
      <v-file-input v-model="formatFile" show-size color="blue-darken-1" label="File input"
                    prepend-icon="mdi-note-plus-outline" bg-color="white" class="mt-1" :rules="fileRules">
        <template #selection="{ fileNames }">
          <template v-for="(fileName, index) in fileNames" :key="fileName">
            <v-chip class="me-2" color="blue-darken-1" label>
              {{ fileName }}
            </v-chip>
          </template>
        </template>
      </v-file-input>
    </template>
    <template v-if="mode === 'role'">
      <v-file-input v-model="roleFile" show-size color="blue-darken-1" label="File input"
                    prepend-icon="mdi-note-plus-outline" bg-color="white" class="mt-1" :rules="fileRules">
        <template #selection="{ fileNames }">
          <template v-for="(fileName, index) in fileNames" :key="fileName">
            <v-chip class="me-2" color="blue-darken-1" label>
              {{ fileName }}
            </v-chip>
          </template>
        </template>
      </v-file-input>
    </template>
    <v-container fluid v-if="mode !== 'format'">
      <v-row>
        <v-col cols="12" sm="6">
          <v-textarea label="Input Text" variant="solo" rows="15" v-model="inputText"></v-textarea>
        </v-col>
        <v-col cols="12" sm="6">
          <v-textarea label="Output Text" variant="solo" rows="15" v-model="outputText"></v-textarea>
        </v-col>
      </v-row>
    </v-container>
    <v-btn class="ml-4 mb-4" @click="process">
      Process
    </v-btn>
    <v-btn class="ml-4 mb-4" @click="reset">
      Reset
    </v-btn>
  </div>
</template>

<style scoped>
  .v-btn {
    margin-left: 1px;
    margin-right: 1px;
  }
</style>
