<template>
  <v-app id="dummy-addon-app" style="max-width: 600px">
    <v-app-bar
        color="#007960"
        dark
        dense
    >
      <v-toolbar-title>Azure ML Integration</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-divider vertical></v-divider>

      <hamburger-menu></hamburger-menu>

    </v-app-bar>

    <!-- Sizes your content based upon application components -->
    <v-main>

      <!-- Provides the application the proper gutter -->
      <div
          class="d-flex flex-column flex-wrap pr-3 pt-5"
          style="background-color: #F6F6F6; opacity: 1"
      >
        <model-inputs></model-inputs>
        <model-action></model-action>
        <model-summary></model-summary>
        <div class="d-flex flex-column justify-center align-center"
             :style="spinner_visible?'height: 120px;': 'display: none !important'">
          <v-progress-circular
              indeterminate
              color="primary"
              size="70"
              width="5"
          ></v-progress-circular>
        </div>
        <div
            class="d-flex flex-column justify-center align-center pb-5"
            :style="spinner_message_visible?'': 'display: none !important'"
        >
          <div :style="message_status==='RUNNING' ? 'color: black;': message_status==='ERROR' ? 'color: #dc3545;' :
      'color: black;'">
            <br>
            <span><b>{{spinner_message_title}} </b>{{spinner_message}}</span>
          </div>
        </div>
      </div>

    </v-main>

  </v-app>
</template>

<style>
  .vuetify-styles .theme--light.v-list-item .v-list-item__action-text,
  .vuetify-styles .theme--light.v-list-item .v-list-item__subtitle {
    color: #212529;
  }

  .vuetify-styles .theme--light.v-list-item:not(.v-list-item--active):not(.v-list-item--disabled) {
    color: #007960 !important;
  }

  .vuetify-styles .v-label {
    font-size: 14px;
  }

  .vuetify-styles .v-application {
    font-family: "Source Sans Pro", "Helvetica Neue", Helvetica, Arial, sans-serif;
  }
</style>