<template>
  <v-card
      class="ml-5 mr-5 mb-5"
      :style="model_summary_visible?'background-color:#F6F6F6; opacity: 1; min-width: 300px':
      'display: none !important'"
  >
    <v-card-title>
      Model Summary
    </v-card-title>
    <v-card-text class="pa-0 pl-5 pr-5">
      <div class="d-flex flex-column">
        <span><b>Model Endpoint: </b>{{endpoint_info}}</span>
        <span><b>Asset Path: </b>{{asset_info}}</span>
        <span><b>Input Signals: </b>{{signals_info}}</span>
        <span><b>Result Signal Name: </b>{{result_signal_info}}</span>
        <div :style="time_range_warning? 'color:red;': ''">
          <span><b>Investigation Range: </b>{{start_info}} - {{end_info}}</span>
        </div>
        <span><b>Deployment Job Name: </b>{{jobname_info}}</span>
        <span><b>Deployment Frequency: </b>{{frequency_info}}</span>
      </div>
    </v-card-text>
    <v-card-text class="pa-0 pl-5 pr-5">
      <div :style="message_type==='SUCCESS' ? 'color: #0455A3;': message_type==='ERROR' ? 'color: #dc3545;' :
      'color: black;'">
        <br>
        <span><b>{{error_title}} </b>{{error_message}}</span>
      </div>
    </v-card-text>
    <div class="d-flex flex justify-end pl-5 pr-5 pb-5">
      <v-btn
          style="text-transform: capitalize;"
          color="success"
          type="submit"
          :disabled="button_disabled"
          :loading="button_loading"
          @click="button_on_click"
      >
        submit
      </v-btn>
    </div>

  </v-card>
</template>