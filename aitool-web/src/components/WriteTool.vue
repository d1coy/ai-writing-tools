<template>
  <div class="item">
    <v-btn>
      Change Tone
    </v-btn>
    <v-btn>
      Adjust Length
    </v-btn>
    <v-btn>
      Summary
    </v-btn>
    <v-btn>
      Customize Role
    </v-btn>
    <v-btn>
      Translate
    </v-btn>
    <v-container fluid>
      <v-row>
        <v-col
          cols="12"
          sm="6"
        >
          <v-textarea
            label="Input Text"
            variant="solo"
          ></v-textarea>
        </v-col>
        <v-col
          cols="12"
          sm="6"
        >
          <v-textarea
            label="Output Text"
            variant="solo"
          ></v-textarea>
        </v-col>
      </v-row>
    </v-container>
    <v-btn>
      Process
    </v-btn>
    <v-btn>
      Reset
    </v-btn>
  </div>
</template>